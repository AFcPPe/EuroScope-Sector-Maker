import json
import os


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


with open('nav/earth_fix.dat', mode='r') as f:
    f.readline()
    f.readline()
    f.readline()
    org = f.read()
    splData = org.split('\n')
    fixData = {}
    for each in splData:
        gp = each.split(' ')
        ng = []
        for i in range(len(gp)):
            if gp[i] == '':
                continue
            ng.append(gp[i])
        if len(ng) < 5:
            continue
        thisJS = {
            'lat': getCored(ng[0], 0),
            'lon': getCored(ng[1], 1),
            'name': ng[2],
            'type': ng[3],
            'sector': ng[4]
        }
        if ng[2] + ng[4] not in fixData:
            fixData[ng[2] + ng[4]] = []
        fixData[ng[2] + ng[4]].append(thisJS)
    with open('./Fix.json', mode='w') as ff:
        json.dump(fixData, ff)

with open('nav/earth_nav.dat', mode='r') as f:
    f.readline()
    f.readline()
    f.readline()
    org = f.read()
    splData = org.split('\n')
    navData = {}
    for each in splData:
        gp = each.split(' ')
        ng = []
        for ee in gp:
            if ee == '':
                continue
            ng.append(ee)
        if len(ng) < 11:
            continue
        thisJS = {
            'lat': getCored(ng[1], 0),
            'lon': getCored(ng[2], 1),
            'freq': ng[4],
            'name': ng[7],
            'type': ng[-1],
            'sector': ng[9],
            'belong': ng[8]
        }
        if ng[7] + ng[9] not in navData:
            navData[ng[7] + ng[9]]=[]
        navData[ng[7] + ng[9]].append(thisJS)
    with open('./Nav.json', mode='w') as ff:
        json.dump(navData, ff)

with open('nav/earth_awy.dat', mode='r') as f:
    f.readline()
    f.readline()
    f.readline()
    org = f.read()
    splData = org.split('\n')
    awyData = {}
    for each in splData:
        gp = each.split(' ')
        ng = []
        # print(gp)
        for ee in gp:
            if ee == '':
                continue
            ng.append(ee)
        if len(ng) != 11:
            # print(len(ng))
            continue
        if ng[2] == '11':
            p1 = (fixData[ng[0] + ng[1]][0]['lat'], fixData[ng[0] + ng[1]][0]['lon'])
        elif ng[2] == '2' or ng[2] == '3':
            p1 = (navData[ng[0] + ng[1]][0]['lat'], navData[ng[0] + ng[1]][0]['lon'])
        if ng[5] == '11':
            p2 = (fixData[ng[3] + ng[4]][0]['lat'], fixData[ng[3] + ng[4]][0]['lon'])
        elif ng[5] == '2' or ng[5] == '3':
            p2 = (navData[ng[3] + ng[4]][0]['lat'], navData[ng[3] + ng[4]][0]['lon'])
        if ng[1] not in awyData:
            awyData[ng[1]]={}
        if ng[10] not in awyData[ng[1]]:
            awyData[ng[1]][ng[10]] = {
                'name':ng[10],
                'fixes':[(p1,p2)]
            }
        else:
            awyData[ng[1]][ng[10]]['fixes'].append((p1,p2))

    for each in awyData:
        for ee in awyData[each]:
            tempL = awyData[each][ee]['fixes']
            awyData[each][ee]['fixes'] = []
            [awyData[each][ee]['fixes'].append(i) for i in tempL if i not in awyData[each][ee]['fixes']]
    with open('./Awy.json',mode='w') as ff:
        json.dump(awyData,ff)

path = './nav/CIFP/'
dirs = os.listdir(path)
sidData = {}
starData = {}
for each in dirs:
    if each[-3:] != 'dat':
        continue
    with open('./nav/CIFP/'+each,'r')as f:
        org = f.read().split('\n')
        for ee in org:
            if ee == '':
                continue
            spl = ee.split(',')
            if spl[0][:3] == 'SID':

                if each[:-4] not in sidData:
                    sidData[each[:-4]] = {}
                if spl[3] not in sidData[each[:-4]]:
                    sidData[each[:-4]][spl[3]] = {}
                if spl[2] not in sidData[each[:-4]][spl[3]]:
                    sidData[each[:-4]][spl[3]][spl[2]] = []
                if spl[4] == ' ' or spl[5] == ' ':
                    continue
                try:
                    fdd = navData[spl[4]+spl[5]]
                    for eeee in fdd:
                        if eeee['belong'] == each[:-4]:
                            sidData[each[:-4]][spl[3]][spl[2]].append((eeee['lat'],eeee['lon']))
                            raise ConnectionError('Finished')
                    for eeee in fdd:
                        if eeee['belong'] == 'ENRT':
                            sidData[each[:-4]][spl[3]][spl[2]].append((eeee['lat'],eeee['lon']))
                            raise ConnectionError('Finished')
                    raise KeyError('Not Found in Nav')
                except KeyError:
                    try:
                        fdd = fixData[spl[4] + spl[5]]
                        for eeee in fdd:
                            if eeee['type'] == each[:-4]:
                                sidData[each[:-4]][spl[3]][spl[2]].append((eeee['lat'], eeee['lon']))
                                raise ConnectionError('Finished')
                        for eeee in fdd:
                            if eeee['type'] == 'ENRT':
                                sidData[each[:-4]][spl[3]][spl[2]].append((eeee['lat'], eeee['lon']))
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
                try:
                    fdd = navData[spl[4]+spl[5]]
                    for eeee in fdd:
                        if eeee['belong'] == each[:-4]:
                            starData[each[:-4]][spl[3]][spl[2]].append((eeee['lat'],eeee['lon']))
                            raise ConnectionError('Finished')
                    for eeee in fdd:
                        if eeee['belong'] == 'ENRT':
                            starData[each[:-4]][spl[3]][spl[2]].append((eeee['lat'],eeee['lon']))
                            raise ConnectionError('Finished')
                    raise KeyError('Not Found in Nav')
                except KeyError:
                    try:
                        fdd = fixData[spl[4] + spl[5]]
                        for eeee in fdd:
                            if eeee['type'] == each[:-4]:
                                starData[each[:-4]][spl[3]][spl[2]].append((eeee['lat'], eeee['lon']))
                                raise ConnectionError('Finished')
                        for eeee in fdd:
                            if eeee['type'] == 'ENRT':
                                starData[each[:-4]][spl[3]][spl[2]].append((eeee['lat'], eeee['lon']))
                                raise ConnectionError('Finished')
                    except KeyError:
                        continue
                    except ConnectionError:
                        continue
                except ConnectionError:
                    continue

            # if spl[0][:3] == 'STA':
            #     if each[:-4] not in starData:
            #         starData[each[:-4]] = {}
            #     if spl[3] not in starData[each[:-4]]:
            #         starData[each[:-4]][spl[3]] = {}
            #     if spl[2] not in starData[each[:-4]][spl[3]]:
            #         starData[each[:-4]][spl[3]][spl[2]] = []
            #     if spl[4]==' ' or spl[5]==' ':
            #         continue
            #     try:
            #         starData[each[:-4]][spl[3]][spl[2]].append((navData[spl[4]+spl[5]]['lat'],navData[spl[4]+spl[5]]['lon']))
            #     except KeyError:
            #         try:
            #             starData[each[:-4]][spl[3]][spl[2]].append((fixData[spl[4] + spl[5]]['lat'], fixData[spl[4] + spl[5]]['lon']))
            #         except KeyError:
            #             continue

with open('SID.json','w')as f:
    json.dump(sidData,f)

with open('STAR.json','w')as f:
    json.dump(starData,f)