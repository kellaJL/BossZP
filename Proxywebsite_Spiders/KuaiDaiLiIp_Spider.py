import bs4
import requests
import re
import UserAgents
import random
class KuaiDaiLiIp_Spider:
    def GetHTMLText(self,url,page=1,code='utf-8'):
        html = ''
        ua={'user-agent':random.choice(UserAgents.agents)}
        url="http://www.kuaidaili.com/free/inha/"+str(page)+'/'
        try:
           r = requests.get(url,headers=ua,timeout=30)
        except:
            pass
        """
        网页请求失败，递归执行
        """
        if 500 <= r.status_code < 600:
            return self.GetHTMLText(url,page)
        r.raise_for_status()
        r.encoding = code
        html = r.text
        return html

    def ParseAndGetInfo(self,url,page=1):
        html=self.GetHTMLText(url,page)
        if html==None:
            return
        soup=bs4.BeautifulSoup(html,'html.parser')
        ip_info=soup.find('table',attrs={'class':'table table-bordered table-striped'})
        key_list=ip_info.find_all('th')
        value_list=ip_info.find_all('td')
        len_list=ip_info.find_all('tr')
        len_list_length=len(len_list)
        
        key_len=len(key_list)
        ip_list=[]#存储获取到的ip列表
        for k in range(len_list_length-1):
           infoDict={}
           for i in range(key_len):
              key=key_list[i].text
              value=str(value_list[i+k*(key_len)].text)
              pat=re.compile(':')
              value1=pat.sub('-',value)
              infoDict[key]=value1
           ip_list.append(infoDict)
           if infoDict['匿名度']=='高匿名':    
              print('proxies:'+str(infoDict))
        #print(ip_list)
        return ip_list


if __name__=="__main__":
   s=KuaiDaiLiIp_Spider()
   url='http://www.kuaidaili.com/free/inha/'
   fpath='D:/s219.txt'
   s.ParseAndGetInfo(url,2)