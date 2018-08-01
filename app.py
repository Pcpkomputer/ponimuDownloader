import requests
import re
import os

def onrequest(link):
    res=pengaturan.session.get(link,headers=payload)
    return res
        
class tidakterlalupenting:
    def suaiubah(self,string):
        result=re.findall(r'([^/]+\w+\d+$)',str(string))[0]
        return result

class rutinitas:
    srtfilename=''
    m3u8filename=''
    def cliAntarMukaUtama(self):
        nav=input('Masukkan URL Ponimu : ')
        _nav=input('Masukkan Resolusi (360|480p|720|1080) : ')
        nav_=input("Kualitas Streaming (worst|best) : ")
        return nav,_nav,nav_
    def parseURL(self,x):
        lastURL=re.findall(r'([^/]\w+\d+$)',str(x))[0]
        activeURL=pengaturan.api_episodes+lastURL
        x=pengaturan.session.get(activeURL,headers=payload)
        print('\nDownloading the assets...')
        child=tidakterlalupenting.suaiubah(x.json()['subtitles'][0]['srtUrl'])
        self.srtfilename=child
        with open('assets/'+child+'.srt','w',encoding='utf-8') as file:
                                 f=requests.get(x.json()['subtitles'][0]['srtUrl']).text
                                 file.write(f)
                                 file.close()
        return x.json()['url']
    def parseM3u8(self, x):
        a=onrequest(x)
        return a.text
    def parseMainFile(self,x):
        res=re.findall(r'RESOLUTION=[^,]+,NAME=\"([^\"]+)\"\s+(.*)',str(x))
        return res
    def checkingNav(self,childMainFile):
        checkingNav_link=''
        for reso,link in childMainFile:
            if re.match(resolusi,str(reso)):
                        checkingNav_link=link
        return pengaturan.api_video+checkingNav_link
    def parseChildFile(self,x):
        res=onrequest(x)
        self.m3u8filename=tidakterlalupenting.suaiubah(str(x))
        with open('m3u8/'+tidakterlalupenting.suaiubah(str(x)),'w') as f:
            f.write(res.text)
            f.close()
        return [self.srtfilename,self.m3u8filename]
        
class pengaturan:
    session=requests.Session()
    absolute=''
    streamlink=os.path.join(absolute,'streamlink.exe')
    videopath='videofile'
    AuthToken=''
    UserAgent=''
    api_episodes='https://api.ponimu.com/api/video-url/'
    api_video='https://video.ponimu.com/hls/'
    def __init__(self):
        with open('pengaturan.ini','r',encoding='utf-8') as file:
            content=file.read()
            res=content.split('_____')
            self.AuthToken=res[0]
            self.UserAgent=res[1]
        with open('streamlink.ini','r',encoding='utf-8') as r:
            self.absolute=r.read()

if __name__=='__main__':
    try:
        ##########
        pengaturan=pengaturan()
        payload={
        'Authorization': pengaturan.AuthToken,
        'User-Agent': pengaturan.UserAgent,
        }
        ##########
        tidakterlalupenting=tidakterlalupenting()
        #############
        #CORROUTINES#
        #############
        rutinitas=rutinitas()
        a, resolusi,kualitas=rutinitas.cliAntarMukaUtama()
        b=rutinitas.parseURL(a)
        c=rutinitas.parseM3u8(b)
        d=rutinitas.parseMainFile(c)
        e=rutinitas.checkingNav(d)
        f=rutinitas.parseChildFile(e)
        #############
        http_headers='Authorization='+pengaturan.AuthToken+';User-Agent='+pengaturan.UserAgent
        n=lambda x: re.findall(r'[^/]+$',str(x))[0]
        cli=pengaturan.streamlink+' '+e+' '+kualitas+' --http-headers "'+http_headers+'"'+' -o '+os.path.dirname(os.path.abspath(__file__))+'\\videofile\\'+str(n(a))+'.ts'
        os.system(cli)
        os.rename('assets/'+rutinitas.srtfilename+'.srt','videofile/'+str(n(a))+'.srt')
       
    except Exception as r:
        print('\nTerjadi kesalahan...')
        
