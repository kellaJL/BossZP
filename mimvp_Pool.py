import requests
import pymysql
import logging
import Proxywebsite_Spiders
from Proxywebsite_Spiders.getproxies import get_from_66ip,get_from_kuaidaili,get_from_xicidaili
REQ_TIMEOUT = 5


class Proxy_Pool:
    def __init__(self):
        self.db = pymysql.connect(
            host='localhost', user='root', passwd='jinlulu666')
        self.cur = self.db.cursor()
        self.cur.execute('use maoyan;')

    def __del__(self):
        """
        析构函数
        """
        self.cur.close()
        self.db.close()

    def push_proxy(self, ip):
        """
        向数据库中插入记录
        :param infoDict:
        :return:
        """

       

        try:
            cur.execute("insert into PROXIES(ip) values(%s)", self.ip)

        except:
            print("插入失败")          
            return
        self.db.commit()

    def del_record(self, ip):
        """
        删除数据库中制定记录
        :param ip:
        :return:
        """
        sql = "delete from PROXIES where IP='{}'".format(ip)
        try:
           self.cur.execute(sql)
           logging.info("删除成功")
           print("删除过期代理IP:"+ip+"成功")
        except:
           print("删除过期代理IP："+ip+"失败")
        self.db.commit()

    def test_connection(self,ip):
        """
        检测代理的有效性
        :param protocol:
        :param ip:
        :param port:
        :return:
        """
        #logging.basicConfig(level=logging.NOTSET)  # 设置日志级别
        #proxies = {protocol: ip + ":" + port}
        proxies = "http://"+ip 
        proxy = {"http": proxies}
        try:
           # OrigionalIP = requests.get("http://icanhazip.com", timeout=REQ_TIMEOUT).content
            MaskedIP = requests.get(
                "http://icanhazip.com", timeout=3, proxies=proxy).content
            if MaskedIP != None:
                print(MaskedIP)
                logging.debug("代理"+proxies+"可用")
                return True
            else:
                print(MaskedIP)
                print("代理"+proxies+"不可用")
                return False
        except:
            return False

 

    def Is_Empty(self):
        """
        查询数据库表kuaidaili是否为空
        """
        sql = "select count(*) from PROXIES;"
        self.cur.execute(sql)
        result = self.cur.fetchone()
        self.db.commit()
        count = result[0]
        if count == 0:
            return True
        else:
            return False

    def clean_nonworking(self):
        """
        循环代理池，逐行测试IP地址端口协议是否可用
        :return:
        """
        sql = "select * from PROXIES;"
        self.cur.execute(sql)
        all = self.cur.fetchall()
        self.db.commit()
        if not all == None:
          for line in all:
            
            ip= line[1]
            isAnonymous = self.test_connection(ip)
            if isAnonymous == False:
                print('delete outdate proxy:'+ip)
                self.del_record(ip)

    def pop_one(self):
        """
        取出表中第一条记录
        """
        sql = "select * from PROXIES limit 1;"
        self.cur.execute(sql)
        line = self.cur.fetchone()
        self.db.commit()
        ip = line[1]
        proxies = "http://"+ip 
        return ip, proxies

    def pop_all(self):
        """
        取出表中所有记录
        """
        sql = "select * from PROXIES;"
        self.cur.execute(sql)
        ips = self.cur.fetchall()
        self.db.commit()
        proxies = []
        for line in ips:
            ip = line[1]
            proxy = "http://"+ip 
            proxies.append(proxy)
        return ips, proxies


if __name__ == "__main__":
    try:
        get_from_xicidaili()
    except:
        print('get_from_xicidaili failed')
    try:
        get_from_66ip()
    except:
        print('get_from_66ip failed')
    # try:
    #     get_from_mimvp()
    # except:
    #     print('get_from_mimvp failed')
    s = Proxy_Pool()
    selection = input("选择")
    selector = eval(selection)
    if selector == 1:
        ip, ik = s.pop_one
        s.test_connection(ip)
        print(ip,ik)
    del s
