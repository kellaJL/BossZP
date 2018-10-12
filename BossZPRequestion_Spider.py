import requests
import json
from bs4 import BeautifulSoup
import UserAgents
import random
import ProxyPool

class BossZP_RequestionSpider():
    def __init__(self,jid,lid):
        self.jid=jid#json请求参数
        self.lid=lid#json请求参数
        self.url="https://www.zhipin.com/view/job/card.json?jid="+str(self.jid)+"&lid="+str(self.lid)
        #https://www.zhipin.com/view/job/card.json?jid=2339af182b9be5111XB70t2_GVQ~&lid=17qKeuLoGkf.search
        self.headers={
           "Host": "www.zhipin.com",
           "Connection": "keep-alive",
           "Pragma": "no-cache",
           "Cache-Control": "no-cache",
           "Accept": "application/json, text/javascript, */*; q=0.01",
           "X-Requested-With": "XMLHttpRequest",
           "User-Agent":random.choice(UserAgents.agents),
           #"Referer": https://www.zhipin.com/c101190100/h_101190100/?query=python&page=2&ka=page-2
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "zh-CN,zh;q=0.9",
           "Cookie": "sid=sem_pz_bdpc_dasou_title; JSESSIONID=""; __c=1539227402; __g=sem_pz_bdpc_dasou_title; __l=l=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title&r=https%3A%2F%2Fwww.baidu.com%2Fs%3Fie%3DUTF-8%26wd%3Dboss%25E7%259B%25B4%25E8%2581%2598&g=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1539076339,1539152693,1539227402; lastCity=101190100; toUrl=https%3A%2F%2Fwww.zhipin.com%2Fc101190100%2Fh_101190100%2F%3Fquery%3Dpython%26page%3D2%26ka%3Dpage-2; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1539249307; __a=1223038.1539076337.1539076344.1539227402.57.3.21.21"
        }
        proxy_pool=ProxyPool.Proxy_Pool()
        self.proxies=[]#代理IP列表
        if not proxy_pool.Is_Empty():
           ip,self.proxies=proxy_pool.pop_all()

    
    # 获取一页数据
    def getOnePage(self):
        proxy = {"http": random.choice(self.proxies)}
        try:
           responses = requests.post(url=self.url, headers=self.headers, proxies=proxy, timeout=30)
        except:
            return 
        if responses.status_code==200:
           return responses.text
        return None
# 解析每一页数据


    def parseOnePage(self,html):
        data = json.loads(html)['html']  # 获取内容
        soup = BeautifulSoup(data,'lxml')
        job_requestion = soup.find("div", {"class": "detail-bottom-text"}).text.strip() # 工作能力要求
        return job_requestion
    
    def main(self):
        html = self.getOnePage()
        job_requestion=self.parseOnePage(html)
        data_list = {}
        data_list["jid"] = self.jid
        data_list["job_requestion"] = job_requestion
        return data_list

if __name__ == "__main__":
    jid = "005be33a8a71228f1XB53dy0GVU~"
    lid = "17srnCo2HlT.search"
    test = BossZP_RequestionSpider(jid, lid)
    dic=test.main()
