import requests
import re
from bs4 import BeautifulSoup
import pymysql
import threading
import time
#from mimvp.mimvpproxy import mimvp_proxy
from Proxywebsite_Spiders.KuaiDaiLiIp_Spider import KuaiDaiLiIp_Spider


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

class IsEnable(threading.Thread):
    def __init__(self,ip):
        super(IsEnable,self).__init__()
        self.ip = ip
        print(ip)
        self.proxies={
        'http':'http://%s'%ip
        }

    def run(self):
        try:
            html=requests.get('http://httpbin.org/ip',proxies=self.proxies,timeout=5).text
            result=eval(html)['origin']
            if len(result.split(','))==2:
                return
            if result in self.ip:
                print("Proxy:"+str(self.proxies)+" 有效")
                self.insert_into_sql()
            self.insert_into_sql()
        except:
            print("Proxy:"+str(self.proxies)+" 无效")
            return

    def insert_into_sql(self):
        db = pymysql.connect(host='localhost', user='root',passwd='jinlulu666', db='maoyan')
        cur = db.cursor()
        try:
            cur.execute("insert into PROXIES(ip) values(%s)",self.ip)
            print(self.ip+"   插入成功")
        except:
            return
        db.commit()
        cur.close()
        db.close()



def get_from_ipcn():
    urls=['http://proxy.ipcn.org/proxya.html','http://proxy.ipcn.org/proxya2.html','http://proxy.ipcn.org/proxyb.html','http://proxy.ipcn.org/proxyb2.html']
    for url in urls:
        try:
            html=requests.get(url,timeout=30).text
        except:
            continue
        ips=re.findall('\d+\.\d+\.\d+\.\d+:\d+',html)
        threadings=[]
        for ip in ips:
            work=IsEnable(ip)
            work.setDaemon(True)
            threadings.append(work)
        for work in threadings:
            work.start()

def get_from_xicidaili():
    urls=['http://www.xicidaili.com/nn/','http://www.xicidaili.com/nn/2','http://www.xicidaili.com/wn/']
    for pageurl in urls:
        try:
            html=requests.get(pageurl,headers=headers,timeout=30).text
        except:
            continue
        table=BeautifulSoup(html,'lxml').find('table',id='ip_list').find_all('tr')
        iplist=[]
        for tr in table[1:]:
            tds=tr.find_all('td')
            ip=tds[1].get_text()+':'+tds[2].get_text()
            iplist.append(ip)
        threadings=[]
        for ip in iplist:
            work=IsEnable(ip)
            work.setDaemon(True)
            threadings.append(work)
        for work in threadings:
            work.start()

def get_from_kxdaili():
    urls=['http://www.kxdaili.com/dailiip/1/%s.html','http://www.kxdaili.com/dailiip/3/%s.html']
    for url in urls:
        page=1
        while page<=10:
            try:
                html=requests.get(url%(page),headers=headers,timeout=30).text.encode('ISO-8859-1').decode('utf-8','ignore')
                page+=1
            except:
                continue
            try:
                table=BeautifulSoup(html,'lxml').find('table').find_all('tr')
            except:
                continue
            iplist=[]
            for tr in table[1:]:
                tds=tr.find_all('td')
                ip = tds[0].get_text() + ':' + tds[1].get_text()
                
                iplist.append(ip)
            threadings=[]
            for ip in iplist:
                work=IsEnable(ip)
                work.setDaemon(True)
                threadings.append(work)
            for work in threadings:
                work.start()

def get_from_66ip():
    urls=['http://www.66ip.cn/nmtq.php?getnum=600&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=&area=0&proxytype=0&api=66ip']
    for pageurl in urls:
        try:
            html=requests.get(pageurl,headers=headers,timeout=30).text
        except:
            continue
        iplist = re.findall('\d+\.\d+\.\d+\.\d+:\d+', html)
        
        threadings=[]
        for ip in iplist:
            work=IsEnable(ip)
            work.setDaemon(True)
            threadings.append(work)
        for work in threadings:
            work.start()
def get_from_kuaidaili():
    s = KuaiDaiLiIp_Spider()
    url='http://www.kuaidaili.com/free/inha/'
    for page in range(10):
        iplist = s.ParseAndGetInfo(url, page + 1)
        threadings = []
        for ip in iplist:
            ip_port=str(ip['IP'])+":"+str(ip["PORT"])
            work=IsEnable(ip_port)
            work.setDaemon(True)
            threadings.append(work)
        for work in threadings:
            work.start()

# def get_from_mimvp():
#     iplist=mimvp_proxy()
#     threadings=[]
#     for ip in iplist:
#         work=IsEnable(ip)
#         work.setDaemon(True)
#         threadings.append(work)
#     for work in threadings:
#         work.start()

if __name__ == '__main__':
 
    flag=True
    while flag:
        # try:
        #     get_from_ipcn()
        # except:
        #     print('get_from_ipcn','failed')
        # try:
        #     get_from_kxdaili()
        # except:
        #     print('get_from_kxdaili','failed')
        try:
            get_from_xicidaili()
        except:
            print('get_from_xicidaili failed')
        try:
            get_from_66ip()
        except:
            print('get_from_66ip failed')
        try:
            get_from_mimvp()
        except:
            print('get_from_mimvp failed')
        flag=False
        #time.sleep(300)

