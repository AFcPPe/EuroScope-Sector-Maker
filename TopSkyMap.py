import json
import os

mapsHeader = '''

COLORDEF:CSID:255:128:0
COLORDEF:CSTAR:0:255:0

SYMBOLDEF:FIX
MOVETO:-4:3
LINETO:0:-4
LINETO:4:3
LINETO:-4:3

SYMBOLDEF:VOR
MOVETO:-4:-4
LINETO:4:-4
LINETO:4:4
LINETO:-4:4
LINETO:-4:-4

SYMBOLDEF:NDB
ARC:0:0:4:0:360

SYMBOLDEF:CSTR
MOVETO:0:0\n


'''


def addZeros(num):
    n = int(num)
    if n < 100 and n > 9:
        num = '0' + num
        return num
    if n >= 1 and n <= 9:
        num = '00' + num
        return num
    if n >= 100:
        return num
    if n >= 0 and n < 1:
        return '000'


def getCored(sit, l):
    groo = sit.split('.')
    if groo[0][0] == '-':
        groo[0] = groo[0][1:]
        if l == 1:
            mark = 'W'
        else:
            mark = 'S'
    else:
        if l == 1:
            mark = 'E'
        else:
            mark = 'N'

    groo[0] = addZeros(groo[0])
    groo[0] = mark + groo[0]
    res = []
    res.append(groo[0])
    groo[1] = '0.' + groo[1]
    groo[1] = str(float(groo[1]) * 60)
    np = groo[1].split('.')
    np[0] = addZeros(np[0])
    res.append(np[0])
    np[1] = '0.' + np[1]
    np[1] = str(float(np[1]) * 60)
    tp = np[1].split('.')
    tp[0] = addZeros(tp[0])
    res.append(tp[0])
    hp = tp[1]
    if float('0.' + hp) <= 0.001:
        hp = '000'
    elif len(hp) >= 3:
        hp = hp[:3]
    elif len(hp) == 2:
        hp = hp + '0'
    elif len(hp) == 1:
        hp = hp + '00'
    else:
        hp = '000'
    res.append(hp)
    xxx = res[0] + '.' + res[1] + '.' + res[2] + '.' + res[3]
    return xxx


def findMap(liss):
    res = mapsHeader

    with open('Nav.json', 'r') as f:
        navData = json.load(f)

    with open('Fix.json', 'r') as f:
        fixData = json.load(f)
    path = './nav/CIFP/'
    dirs = os.listdir(path)

    for region in liss:
        sidData = {}
        starData = {}
        for each in dirs:
            if each[:2] != region[:2]:
                continue
            if each[-3:] != 'dat':
                continue
            with open('./nav/CIFP/' + each, 'r') as f:
                org = f.read().split('\n')
                for ee in org:
                    if ee == '':
                        continue
                    spl = ee.split(',')

                    abo = ''
                    loa = ''
                    spd = ''
                    if len(spl)>=22 and spl[26]!=' ':
                        if spl[26]=='-':
                            spl[26]='MAX'
                        if spl[26]=='+':
                            spl[26]='MIN'
                        spd = spl[26]+spl[27]+'kt'
                    if len(spl) >= 22 and spl[23][0]!=' 'and spl[24][0]!=' ':
                        if len(spl[23]) >=2 and spl[23][:2]=='FL':
                            spl[23] = str(int(spl[23][2:])*100)
                        if len(spl[24]) >=2 and spl[24][:2]=='FL':
                            spl[24] = str(int(spl[24][2:])*100)
                        spl[23] = str(int(round(int(spl[23])*0.3048,-2)))
                        spl[24] = str(int(round(int(spl[24]) * 0.3048, -2)))
                        if spl[22] == '+':
                            abo = spl[23] + '+'
                        if spl[22] == '-':
                            loa = spl[23] + '-'
                        if spl[22] == 'B':
                            abo = spl[24] + '+'
                            loa = spl[23] + '-'
                    if spl[0][:3] == 'SID':
                        if each[:-4] not in sidData:
                            sidData[each[:-4]] = {}
                        if spl[3] not in sidData[each[:-4]]:
                            sidData[each[:-4]][spl[3]] = {}
                        if spl[2] not in sidData[each[:-4]][spl[3]]:
                            sidData[each[:-4]][spl[3]][spl[2]] = []
                        if spl[4] == ' ' or spl[5] == ' ':
                            continue
                        if spl[1] != '5' and spl[1] != '6' and spl[1] != '4':
                            continue
                        try:
                            fdd = navData[spl[4] + spl[5]]
                            for eeee in fdd:
                                if eeee['belong'] == each[:-4]:
                                    sidData[each[:-4]][spl[3]][spl[2]].append(
                                        (eeee['lat'], eeee['lon'], eeee['name'], 'nav', eeee['type'],abo,loa,spd))
                                    raise ConnectionError('Finished')
                            for eeee in fdd:
                                if eeee['belong'] == 'ENRT':
                                    sidData[each[:-4]][spl[3]][spl[2]].append(
                                        (eeee['lat'], eeee['lon'], eeee['name'], 'nav', eeee['type'],abo,loa,spd))
                                    raise ConnectionError('Finished')
                            raise KeyError('Not Found in Nav')
                        except KeyError:
                            try:
                                fdd = fixData[spl[4] + spl[5]]
                                for eeee in fdd:
                                    if eeee['type'] == each[:-4]:
                                        sidData[each[:-4]][spl[3]][spl[2]].append(
                                            (eeee['lat'], eeee['lon'], eeee['name'], 'fix','',abo,loa,spd))
                                        raise ConnectionError('Finished')
                                for eeee in fdd:
                                    if eeee['type'] == 'ENRT':
                                        sidData[each[:-4]][spl[3]][spl[2]].append(
                                            (eeee['lat'], eeee['lon'], eeee['name'], 'fix','',abo,loa,spd))
                                        raise ConnectionError('Finished')
                            except KeyError:
                                continue
                            except ConnectionError:
                                continue
                        except ConnectionError:
                            continue

                    if spl[0][:3] == 'STA':

                        if each[:-4] not in starData:
                            starData[each[:-4]] = {}
                        if spl[3] not in starData[each[:-4]]:
                            starData[each[:-4]][spl[3]] = {}
                        if spl[2] not in starData[each[:-4]][spl[3]]:
                            starData[each[:-4]][spl[3]][spl[2]] = []
                        if spl[4] == ' ' or spl[5] == ' ':
                            continue
                        if spl[1] != '5' and spl[1] != '6' and spl[1] != '4':
                            continue
                        try:
                            fdd = navData[spl[4] + spl[5]]
                            for eeee in fdd:
                                if eeee['belong'] == each[:-4]:
                                    starData[each[:-4]][spl[3]][spl[2]].append(
                                        (eeee['lat'], eeee['lon'], eeee['name'], 'nav', eeee['type'],abo,loa,spd))
                                    raise ConnectionError('Finished')
                            for eeee in fdd:
                                if eeee['belong'] == 'ENRT':
                                    starData[each[:-4]][spl[3]][spl[2]].append(
                                        (eeee['lat'], eeee['lon'], eeee['name'], 'nav', eeee['type'],abo,loa,spd))
                                    raise ConnectionError('Finished')
                            raise KeyError('Not Found in Nav')
                        except KeyError:
                            try:
                                fdd = fixData[spl[4] + spl[5]]
                                for eeee in fdd:
                                    if eeee['type'] == each[:-4]:
                                        starData[each[:-4]][spl[3]][spl[2]].append(
                                            (eeee['lat'], eeee['lon'], eeee['name'], 'fix','',abo,loa,spd))
                                        raise ConnectionError('Finished')
                                for eeee in fdd:
                                    if eeee['type'] == 'ENRT':
                                        starData[each[:-4]][spl[3]][spl[2]].append(
                                            (eeee['lat'], eeee['lon'], eeee['name'], 'fix','',abo,loa,spd))
                                        raise ConnectionError('Finished')
                            except KeyError:
                                continue
                            except ConnectionError:
                                continue
                        except ConnectionError:
                            continue

        for p in starData:
            n = starData[p].copy()
            for l in n:
                if l == ' ':
                    for ggr in starData[p][l]:
                        for ppl in n:
                            if ppl == ' ':
                                continue
                            if ggr in starData[p][ppl]:
                                for ddl in range(len(starData[p][l][ggr])):
                                    starData[p][ppl][ggr].insert(ddl, starData[p][l][ggr][ddl])
                if l == 'ALL':
                    for ggr in starData[p][l]:
                        for ppl in n:
                            if ppl == ' ':
                                continue
                            starData[p][ppl][ggr] = starData[p][l][ggr]

        for p in sidData:
            n = sidData[p].copy()
            for l in n:
                if l == ' ':
                    for ggr in sidData[p][l]:
                        for ppl in n:
                            if ppl == ' ':
                                continue
                            if ggr in sidData[p][ppl]:
                                for ddl in range(len(sidData[p][l][ggr])):
                                    sidData[p][ppl][ggr].append(sidData[p][l][ggr][ddl])
                if l == 'ALL':
                    for ggr in sidData[p][l]:
                        for ppl in n:
                            if ppl == ' ':
                                continue
                            sidData[p][ppl][ggr] = sidData[p][l][ggr]

        for p in starData:
            n = starData[p].copy()
            for l in n:
                if l[-1] == 'B':
                    for ggr in starData[p][l]:
                        if l[:-1] + 'R' not in starData[p]:
                            starData[p][l[:-1] + 'R'] = {}
                        if l[:-1] + 'L' not in starData[p]:
                            starData[p][l[:-1] + 'L'] = {}
                        starData[p][l[:-1] + 'R'][ggr] = starData[p][l][ggr]
                        starData[p][l[:-1] + 'L'][ggr] = starData[p][l][ggr]
        for p in sidData:
            n = sidData[p].copy()
            for l in n:
                if l[-1] == 'B':
                    for ggr in sidData[p][l]:
                        if l[:-1] + 'R' not in sidData[p]:
                            sidData[p][l[:-1] + 'R'] = {}
                        if l[:-1] + 'L' not in sidData[p]:
                            sidData[p][l[:-1] + 'L'] = {}
                        sidData[p][l[:-1] + 'R'][ggr] = sidData[p][l][ggr]
                        sidData[p][l[:-1] + 'L'][ggr] = sidData[p][l][ggr]

        coAll = {}
        for eddd in sidData:
            arp = sidData[eddd]
            for eqqq in arp:
                rees = set([])
                cstr = {}
                rwya = arp[eqqq]
                res += 'MAP:' + eddd + '-' + eqqq + '-SID\n'
                res += 'FOLDER:' + region
                res += '\nCOLOR:CSID\nACTIVE:'
                res += 'RWY:ARR:*:DEP:' + eddd + eqqq[2:] + '\n'
                res += 'ZOOM:8\n\n'
                for eaaa in rwya:
                    poss = rwya[eaaa]
                    for i in range(len(poss)):
                        pointsss = poss[i]
                        if pointsss[2] not in cstr:
                            cstr[pointsss[2]] = set()
                        if pointsss[3] == 'fix':
                            rees.add('SYMBOL:FIX:' + pointsss[2] + ':' + pointsss[2] + ':0:12\n')
                        if pointsss[3] == 'nav':
                            if pointsss[4][:3] == 'NDB':
                                rees.add('SYMBOL:NDB:' + pointsss[2] + ':' + pointsss[2] + ':0:12\n')
                            if pointsss[4][:3] == 'VOR':
                                rees.add('SYMBOL:VOR:' + pointsss[2] + ':' + pointsss[2] + ':0:12\n')
                        if pointsss[5] != '':
                            cstr[pointsss[2]].add('SYMBOL:CSTR:' + pointsss[2] + ':' + pointsss[
                                5] + ' for ' + eaaa + ' rwy ' + eqqq + ':0:')
                        if pointsss[6] != '':
                            cstr[pointsss[2]].add('SYMBOL:CSTR:' + pointsss[2] + ':' + pointsss[
                                6] + ' for ' + eaaa + ' rwy ' + eqqq + ':0:')
                        if pointsss[7] != '':
                            cstr[pointsss[2]].add('SYMBOL:CSTR:' + pointsss[2] + ':' + pointsss[
                                7] + ' for ' + eaaa + ' rwy ' + eqqq + ':0:')
                        if i == 0:
                            continue
                        rees.add('LINE:' + poss[i][0] + ':' + poss[i][1] + ':' + poss[i - 1][0] + ':' + poss[i - 1][
                            1] + '\n')
                # for i in cstr:
                #     if i not in coAll:
                #         coAll[i] = 24
                #     for j in iter(cstr[i]):
                #         res+= j+str(coAll[i])+'\n'
                #         coAll[i]+=12
                for i in iter(rees):
                    res += i


        for eddd in starData:
            arp = starData[eddd]

            for eqqq in arp:
                if eqqq == ' ':
                    continue
                rees = set([])
                cstr = {}
                rwya = arp[eqqq]
                res += 'MAP:' + eddd + '-' + eqqq + '-STAR\n'
                res += 'FOLDER:' + region
                res += '\nCOLOR:CSTAR\nACTIVE:'
                res += 'RWY:ARR:' + eddd + eqqq[2:] + ':DEP:*\n'
                res += 'ZOOM:8\n\n'
                for eaaa in rwya:

                    poss = rwya[eaaa]
                    for i in range(len(poss)):
                        pointsss = poss[i]
                        if pointsss[2] not in cstr:
                            cstr[pointsss[2]] = set()
                        if pointsss[3] == 'fix':
                            rees.add('SYMBOL:FIX:' + pointsss[2] + ':' + pointsss[2] + ':0:12\n')
                        if pointsss[3] == 'nav':
                            if pointsss[4][:3] == 'NDB':
                                rees.add('SYMBOL:NDB:' + pointsss[2] + ':' + pointsss[2] + ':0:12\n')
                            if pointsss[4][:3] == 'VOR':
                                rees.add('SYMBOL:VOR:' + pointsss[2] + ':' + pointsss[2] + ':0:12\n')
                        if pointsss[5] != '':
                            cstr[pointsss[2]].add('SYMBOL:CSTR:' + pointsss[2] + ':' + pointsss[5] +' for '+eaaa+' rwy ' + eqqq + ':0:')
                        if pointsss[6] != '':
                            cstr[pointsss[2]].add('SYMBOL:CSTR:' + pointsss[2] + ':' + pointsss[6] +' for '+eaaa+' rwy ' + eqqq + ':0:')
                        if pointsss[7] != '':
                            cstr[pointsss[2]].add('SYMBOL:CSTR:' + pointsss[2] + ':' + pointsss[7] +' for '+eaaa+' rwy ' + eqqq + ':0:')
                        if i == 0:
                            continue
                        rees.add('LINE:' + poss[i][0] + ':' + poss[i][1] + ':' + poss[i - 1][0] + ':' + poss[i - 1][
                            1] + '\n')
                # for i in cstr:
                #     if i not in coAll:
                #         coAll[i] = 24
                #     for j in iter(cstr[i]):
                #         res += j + str(coAll[i]) + '\n'
                #         coAll[i] += 12

                for i in iter(rees):
                    res += i



        with open('TopSkyMaps.txt', 'w') as f:
            f.write(res)


findMap(['ZGZU', 'ZSHA','ZWUQ','ZHWH','ZBPE','ZYSH','ZJSA','ZKPM','ZUUU','ZLHW','ZMUB '])
