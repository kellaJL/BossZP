from requests import post
from bs4 import BeautifulSoup
import UserAgents
import os
import random
from logging import error
import redis
from time import sleep
import ProxyPool
import PushData2MySql
class BossZP_Spider:
    def __init__(self):
        self.start_url = "https://www.zhipin.com/"
        self.cities_code = {"深圳": "c101280600-p100109/h_101280600/", "上海": "c101020100-p100109/h_101020100/", "北京": "c101010100/h_101010100/",
                            "南京": "c101190100/h_101190100/", "杭州": "c101210100/h_101210100/"}  # 北京，南京，杭州
        self.headers = {
		    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Cache-Control': "no-cache",
            'Connection': "keep-alive",
            'Cookie': "sid=sem_pz_bdpc_dasou_title; JSESSIONID=""; __g=sem_pz_bdpc_dasou_title; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1539076339; __c=1539076344; __l=r=https%3A%2F%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title&l=%2Fwww.zhipin.com%2Fjob_detail%2F%3Fka%3Dheader-job&g=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_ti; lastCity=101190100; toUrl=https%3A%2F%2Fwww.zhipin.com%2Fc101190100%2Fh_101190100%2F%3Fquery%3Dpython%26page%3D2; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1539130799; __a=1223038.1539076337.1539076337.1539076344.24.2.23.24",
            'Host': "www.zhipin.com",
            'Pragma': "no-cache",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent': random.choice(UserAgents.agents)
        }
        
        pool = redis.ConnectionPool(host='localhost', port=6379)
        self.conn = redis.Redis(connection_pool=pool)
        self.proxy_pool=ProxyPool.Proxy_Pool()
        self.proxies = []
        self.ip=[]
        if not self.proxy_pool.Is_Empty():
           self.ip,self.proxies=self.proxy_pool.pop_all()
        
        



    def parsePage(self,info):
        #info=soup.find_all("div",{"class":"job-primary"})
        info_list=[]
        try:
          for each in info:
            info_dict={}
            info_dict["jid"]=each.find("h3",{"class":"name"}).find("a").attrs["data-jid"]
            info_dict["lid"]=each.find("h3",{"class":"name"}).find("a").attrs["data-lid"]
            info_dict["job_title"]=each.find("div",{"class":"job-title"}).text#岗位
            info_dict["job_red"]=each.find("span",{"class":"red"}).text#薪资
            #info_dict["job_requestion"]=each.find("div",{"class":"detail-bottom-text"}).text[1:]#工作能力要求
            
            l_e_e=each.find("div",{"class":"info-primary"}).find("p").text

            info_dict["job_location"]=l_e_e#工作地点
            
            info_dict["job_experience"]=l_e_e#工作经验
            info_dict["e_b"]=l_e_e#学历要求
            #self.conn.lpush("bzp_list",info_dict)
            # print(job_title,job_red,job_requestion,job_location,job_experience,e_b)
            info_list.append(info_dict)
            print(info_dict)
        except:
          error("error!")
          pass
        PushData2MySql.pushData_1(info_list)#将数据导入数据库
        return info_list


    def getInfo(self,city,page,query="python"):
        #url=self.start_url+self.cities_code[city]+"?query=python&page=2&ka=page-2"
        url=self.start_url+self.cities_code[city]
        
        post_data = {
            "?query": query,
            "page": str(page),
            "ka": "page-"+str(page)
        }
        ip_choose=random.choice(self.ip)
        proxies = ip_choose[3]+"://"+ip_choose[0] + ":" + ip_choose[1]
        proxy={"http":proxies}
        pages=post(url,data=post_data,headers=self.headers,proxies=proxy,timeout=20)
        #pages=post(url,headers=self.headers,proxies=proxy,timeout=20)
        print(pages.status_code)
        soup=BeautifulSoup(pages.text,"lxml")
        info = soup.find_all("div", {"class": "job-primary"})
        
        if len(info) == 0:
            self.proxy_pool.del_record(ip_choose[0])
            return 0

        self.parsePage(info)
        return 1
    

    def main(self,city,page=1):
        while page<10:
            try:
                flag=self.getInfo(city,page)
                if(flag==1):
                   page += 1
                sleep(5)     
            except:
                error("Spider"+str(page)+" get problems")
                pass

if __name__=="__main__":
    s=BossZP_Spider()
    s.main("南京",1)
