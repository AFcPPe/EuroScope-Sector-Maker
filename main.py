import os

def getSID(code):
    path = './nav/CIFP/'
    dirs = os.listdir(path)
    result = '[SID]\n'
    for each in dirs:
        if each[:2]==code:
            with open(path+each,'r')as f:
                lines = f.read().split('\n')
                currP = ''
                for ee in lines:
                    spl = ee.split(',')
                    if spl[0][:3]=='SID':
                        if spl[2] == currP:
                            pass
                        else:
                            currP = spl[2]
                        fix = findNav(spl[4], code)
                        # print(spl[4],fix)


def getFix(code):
    with open('nav/earth_fix.dat', mode='r') as f:
        f.readline()
        f.readline()
        f.readline()
        origin_data = f.read()
    line_data = origin_data.split('\n')
    group_data = []
    n = 0
    for each in line_data:
        group_data.append(each.split(' '))
        n = n + 1
    group_fixed = []
    n = 0
    for each in group_data:
        group_fixed.append([])
        for e in each:
            if e != '':
                group_fixed[n].append(e)
        n = n + 1
    result = '[FIXES]\n'
    for each in group_fixed:
        try:
            if each[4] == code:
                result = result + each[2] + ' ' + getCored(each[0], 0) + ' ' + getCored(each[1], 1) + '\n'
        except IndexError:
            continue

    return result


def getVOR(code):
    with open('nav/earth_nav.dat', mode='r') as f:
        f.readline()
        f.readline()
        f.readline()
        origin_data = f.read()
    line_data = origin_data.split('\n')
    group_data = []
    n = 0
    for each in line_data:
        group_data.append(each.split(' '))
        n = n + 1
    group_fixed = []
    n = 0
    for each in group_data:
        group_fixed.append([])
        for e in each:
            if e != '':
                group_fixed[n].append(e)
        n = n + 1
    result = '[VOR]\n'
    for each in group_fixed:
        try:
            if each[9] == code and each[11] == 'VOR/DME':
                result = result + each[7] + ' ' + str(float(each[4]) / 100) + ' ' + getCored(each[1],
                                                                                             0) + ' ' + getCored(
                    each[2], 1) + '\n'
        except IndexError:
            continue

    return result


def getNDB(code):
    with open('nav/earth_nav.dat', mode='r') as f:
        f.readline()
        f.readline()
        f.readline()
        origin_data = f.read()
    line_data = origin_data.split('\n')
    group_data = []
    n = 0
    for each in line_data:
        group_data.append(each.split(' '))
        n = n + 1
    group_fixed = []
    n = 0
    for each in group_data:
        group_fixed.append([])
        for e in each:
            if e != '':
                group_fixed[n].append(e)
        n = n + 1
    result = '[NDB]\n'
    for each in group_fixed:
        try:
            if each[9] == code and each[11] == 'NDB':
                result = result + each[7] + ' ' + each[4] + ' ' + getCored(each[1], 0) + ' ' + getCored(each[2],1) + '\n'
        except IndexError:
            continue

    return result


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
    gp = sit.split('.')
    if gp[0][0] == '-':
        gp[0] = gp[0][1:]
        if l == 1:
            mark = 'W'
        else:
            mark = 'S'
    else:
        if l == 1:
            mark = 'E'
        else:
            mark = 'N'

    gp[0] = addZeros(gp[0])
    gp[0] = mark + gp[0]
    res = []
    res.append(gp[0])
    gp[1] = '0.' + gp[1]
    gp[1] = str(float(gp[1]) * 60)
    np = gp[1].split('.')
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


def findAirways(code):
    with open('2208/earth_awy.dat', mode='r') as f:
        f.readline()
        f.readline()
        f.readline()
        origin_data = f.read()
    line_data = origin_data.split('\n')
    group_data = []
    n = 0
    for each in line_data:
        group_data.append(each.split(' '))
        n = n + 1
    group_fixed = []
    n = 0
    for each in group_data:
        group_fixed.append([])
        for e in each:
            if e != '':
                group_fixed[n].append(e)
        n = n + 1

    for each in group_fixed:
        try:
            if each[1] == code or each[4] == code:
                print(each[10], each[0], each[3])
        except IndexError:
            continue


def useCored(str):
    group = str.split(' ')
    final = []
    for each in group:
        if each != '':
            final.append(each)
    x = getCored(final[0], 0)
    y = getCored(final[1], 1)
    print(x, y)


def findFix(name,code):
    with open('nav/earth_fix.dat', mode='r') as f:
        f.readline()
        f.readline()
        f.readline()
        origin_data = f.read()
    line_data = origin_data.split('\n')
    for each in line_data:
        gp = each.split(' ')
        # print(gp)
        try:
            if gp[5] == name and gp[7] == code:
                return getCored(gp[1], 0), getCored(gp[3], 1)
        except IndexError:
            return None
    return None


def findNav(name,code):
    with open('nav/earth_nav.dat', mode='r') as f:
        f.readline()
        f.readline()
        f.readline()
        origin_data = f.read()
    line_data = origin_data.split('\n')
    for each in line_data:
        gp = each.split(' ')
        # print(gp)
        try:
            print(gp)
            # if gp[5] == name and gp[7] == code:
            #     return getCored(gp[1], 0), getCored(gp[3], 1)
        except IndexError:
            return None
    return None

#
# def getAirort(code):
#     path = './nav/CIFP/'
#     dirs = os.listdir(path)
#     result = '[AIRPORT]\n'
#     for each in dirs:
#         if each[:2]==code:
#             with open(path+each,'r')as f:
#                 lines = f.read().split('\n')
#             rwys ={}
#             for ee in lines:
#                 if ee[:3]=='RWY':
#                     print(ee[6:8],ee[8])
#                     ls = ee.split(';')[1].split(',')
#                     latiti = proceedCloaCord(ls[0])
#                     longigi = proceedCloaCord(ls[1])
#                     rwys[ee[6:9]] = {'num':int(ee[6:8]),'plc':ee[8]}
#                     # print(latiti,longigi)
#
#
# def proceedCloaCord(cor):
#     pref = cor[0]
#     suff = cor[1:]
#     if len(suff) == 8:
#         return pref+suff[0:2]+'.'+suff[2:4]+'.'+suff[4:6]+ '.' + suff[6:8]
#     if len(suff) == 9:
#         return pref+suff[0:3] + '.' + suff[3:5] + '.' + suff[5:7]+ '.' + suff[7:9]


def read(code, file):
    ndb = getNDB(code)
    vor = getVOR(code)
    fix = getFix(code)
    sid = getSID(code)
    # airports = getAirort(code)
    with open('' + file + '.sct', 'w') as f:
        f.write(vor)
        f.write('\n\n\n')
        f.write(ndb)
        f.write('\n\n\n')
        f.write(fix)


read('ZB', 'ZBPE')
read('ZY', 'ZYSH')
read('ZB', 'ZBPE')
read('ZY', 'ZYSH')
read('ZB', 'ZBPE')
read('ZY', 'ZYSH')
# with open('result.sct', mode='r') as f:
#     add = f.read()
# print(add)

# while 1:
#     hh = input()
#     useCored(hh)
