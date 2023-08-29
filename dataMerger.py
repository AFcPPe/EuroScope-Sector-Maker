import os
navi = '2212'
color = '''
#define MVA 6908265
#define ApronAsph 3815994
#define ApronConc 5658198
#define Building 7730
#define Coastline 8421504
#define Grass 2245678
#define GroundArea 128
#define GroundMark 49087
#define GroundSector 7730
#define Helicopter 12615680
#define HoldPoint 157
#define Range 15110456
#define Runway 7260
#define RunwayMark 7730
#define RunwayShoulder 3815994
#define SpecialArea 128
#define Taxiin 16755200
#define Taxiline 7631988
#define Taxiout 43605
#define Terminal 29855
#define TerminalVech 6908265\n
'''


def getEle(head,scts):
    subs = scts[scts.find(head) + len(head)+1:]
    num = subs.find('[')
    if num == -1:
        return subs+'\n'
    return subs[:subs.find('[')]+'\n'



def merge(name,mode):
    global color
    region = '[REGIONS]\n'
    geo = '[GEO]\n'
    runway = '[RUNWAY]\n'
    path = 'src/'+name[:2]
    dirs = os.listdir(path)
    if mode == 'sct':
        info = name + ' ' + navi + ' SKYLINE(C)\n'+name+'_CTR\n'+name+'N022.36.35.999\nE108.10.23.999\n'+'150\n51.323\n5.800\n1\n\n\n'
        for each in dirs:
            if each[-3:] == 'sct':
                if each[:4]==name:
                    continue
                print(each)
                with open('src/'+name[:2]+'/'+each,'r',encoding='utf-8')as f:
                    scts = f.read()
                region = region + getEle('[REGIONS]',scts)
                geo = geo + getEle('[GEO]', scts)
                runway = runway + getEle('[RUNWAY]', scts)
        with open('merge/'+name+'.sct','w') as f:
            with open('src/'+name[:2]+'/'+name+'.sct','r')as fa:
                f.write(color)
                f.write(info)
                f.write(fa.read()+'\n')
                f.write(region)
                f.write(geo)
                f.write(runway)
    if mode == 'ese':
        frtx = '[FREETEXT]\n'
        for each in dirs:
            if each[-3:] == 'ese':
                if each[:4]==name:
                    continue
                print(each)
                with open('src/'+name[:2]+'/'+each,'r',encoding='utf-8')as f:
                    eses = f.read()
                subs = eses[eses.find('[FREETEXT]')+11:]+'\n\n'
                frtx+=subs
        with open('merge/'+name+'.ese','w') as f:
            f.write(frtx)


merge('ZBPE','sct')
merge('ZGZU','sct')
merge('ZHWH','sct')
merge('ZJSA','sct')
merge('ZLHW','sct')
merge('ZPKM','sct')
merge('ZSHA','sct')
merge('ZUCD','sct')
merge('ZWUQ','sct')
merge('ZYSH','sct')

merge('ZBPE','ese')
merge('ZGZU','ese')
merge('ZHWH','ese')
merge('ZJSA','ese')
merge('ZLHW','ese')
merge('ZPKM','ese')
merge('ZSHA','ese')
merge('ZUCD','ese')
merge('ZWUQ','ese')
merge('ZYSH','ese')