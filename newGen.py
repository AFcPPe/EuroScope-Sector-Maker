import json
fixData = {}
navData = {}
awyData = {}
sidData = {}
starData = {}
with open('Fix.json','r') as f:
    fixData = json.load(f)

with open('Nav.json','r') as f:
    navData = json.load(f)

with open('Awy.json','r') as f:
    awyData = json.load(f)

with open('SID.json','r')as f:
    sidData = json.load(f)

with open('STAR.json','r')as f:
    starData = json.load(f)

def getVOR(code):
    global fixData,navData,awyData,sidData,starData
    result = '[VOR]\n'
    inoCF = []
    for each in navData:
        fdd = navData[each]
        for e in fdd:
            if e['type'][:3] == 'VOR' and (e['sector'] == code or code=='all'):
                inoCF.append(e['name'] + ' ' + str(float(e['freq'])/100)+' ' + e['lat']+ ' ' + e['lon']+'\n')
    inoCF = set(inoCF)
    for e in inoCF:
        result += e
    return result

def getNDB(code):
    global fixData,navData,awyData,sidData,starData
    result = '[NDB]\n'
    inoCF = []
    for each in navData:
        fdd = navData[each]
        for e in fdd:
            if e['type'][:3] == 'NDB' and (e['sector'] == code or code=='all'):
                inoCF.append(e['name'] + ' ' + e['freq']+' ' + e['lat']+ ' ' + e['lon']+'\n')
    inoCF = set(inoCF)
    for e in inoCF:
        result+=e
    return result

def getFixes(code):
    global fixData, navData, awyData,sidData,starData
    result = '[FIXES]\n'
    inoCF = []
    for each in fixData:
        fdd = fixData[each]
        for e in fdd:
            if e['sector'] == code or code=='all':
                inoCF.append(e['name'] + ' ' + e['lat']+ ' ' + e['lon']+'\n')
    inoCF = set(inoCF)
    for e in inoCF:
        result += e
    return result

def getAirway(code):
    global fixData, navData, awyData,sidData,starData
    result = '[HIGH AIRWAY]\n'
    for each in awyData[code]:
        for ee in awyData[code][each]['fixes']:
            result += awyData[code][each]['name'] + ' '
            result += ee[0][0] + ' '
            result += ee[0][1] + ' '
            result += ee[1][0] + ' '
            result += ee[1][1] + '\n'
    # print(result)
    return result

def getAllAirway():
    global fixData, navData, awyData,sidData,starData
    result = '[HIGH AIRWAY]\n'
    for code in awyData:
        for each in awyData[code]:
            for ee in awyData[code][each]['fixes']:
                result += awyData[code][each]['name'] + ' '
                result += ee[0][0] + ' '
                result += ee[0][1] + ' '
                result += ee[1][0] + ' '
                result += ee[1][1] + '\n'
    # print(result)
    return result

def getSID(code):
    global fixData, navData, awyData,sidData,starData
    result = '[SID]\n'
    for each in sidData:
        if each[:2] ==code or code=='all':
            erwy = sidData[each]
            for ee in erwy:
                for eee in erwy[ee]:
                    epoint = erwy[ee][eee]
                    result += each + ' ' + ee + ' ' + eee+'\t'
                    for i in range(len(epoint)-1):
                        result+=epoint[i][0]+' '+epoint[i][1]+' '+epoint[i+1][0]+' '+epoint[i+1][1]+'\n\t\t\t\t\t'
                        # print(eeee)
                    result+='\n'
    return result

def getSTAR(code):
    global fixData, navData, awyData,sidData,starData
    result = '[STAR]\n'
    for each in starData:
        if each[:2] ==code or code=='all':
            erwy = starData[each]
            for ee in erwy:
                for eee in erwy[ee]:
                    epoint = erwy[ee][eee]
                    result += each + ' ' + ee + ' ' + eee+'\t'
                    for i in range(len(epoint)-1):
                        result+=epoint[i][0]+' '+epoint[i][1]+' '+epoint[i+1][0]+' '+epoint[i+1][1]+'\n\t\t\t\t\t'
                        # print(eeee)
                    result+='\n'
    return result


def read(code,file):
    ndb = getNDB(code)
    vor = getVOR(code)
    fix = getFixes(code)
    awy = getAirway(code)
    sid = getSID(code)
    star = getSTAR(code)
    # airports = getAirort(code)
    with open('' + file + '.sct', 'w') as f:
        f.write(vor)
        f.write('\n\n\n')
        f.write(ndb)
        f.write('\n\n\n')
        f.write(fix)
        f.write('\n\n\n')
        f.write(awy)
        f.write('\n\n\n')
        f.write(sid)
        f.write('\n\n\n')
        f.write(star)

def readAll(file):
    ndb = getNDB('all')
    vor = getVOR('all')
    fix = getFixes('all')
    awy = getAllAirway()
    sid = getSID('all')
    star = getSTAR('all')
    # airports = getAirort(code)
    with open('' + file + '.sct', 'w') as f:
        f.write(vor)
        f.write('\n\n\n')
        f.write(ndb)
        f.write('\n\n\n')
        f.write(fix)
        f.write('\n\n\n')
        f.write(awy)
        f.write('\n\n\n')
        f.write(sid)
        f.write('\n\n\n')
        f.write(star)

readAll('src/SUPS/SUP')
# read('ZB','src/ZB/ZBPE')
# read('ZG','src/ZG/ZGZU')
# read('ZH','src/ZH/ZHWH')
# read('ZJ','src/ZJ/ZJSA')
# read('ZL','src/ZL/ZLHW')
# read('ZP','src/ZP/ZPKM')
# read('ZS','src/ZS/ZSHA')
# read('ZU','src/ZU/ZUCD')
# read('ZW','src/ZW/ZWUQ')
# read('ZY','src/ZY/ZYSH')

# read('ZB','ZBPE')