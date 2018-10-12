import requests
import pymysql
import logging
REQ_TIMEOUT=5
class Proxy_Pool:
    def __init__(self):
        self.db = pymysql.connect(host='localhost', user='root', passwd='')
        self.cur = self.db.cursor()
        self.cur.execute('use maoyan;')

    def __del__(self):
        """
        析构函数
        """
        self.cur.close()
        self.db.close()

    def add_proxy(self,ip_list):
        """
        向数据库中插入记录
        :param infoDict:
        :return:
        """
        
        illegalValues=[]
               
        #批量插入数据
        for key in ip_list:
           ls=list(key.values())
           try:
               self.cur.execute("""insert into `kuaidaili`(`IP`,`port`,`匿名度`,`类型`,`位置`,`响应速度`,`最后验证时间`) values(%s,%s,%s,%s,%s,%s,%s);""", ls)
               
           except:
               illegalValues.append(key)
               print(ip_list.index(key))
               pass
        self.db.commit()

    def del_record(self,ip):
        """
        删除数据库中制定记录
        :param ip:
        :return:
        """
        sql="delete from kuaidaili where IP='{}'".format(ip)
        try:
           self.cur.execute(sql)
           logging.info("删除成功")
           print("删除过期代理IP:"+ip+"成功")
        except:
           print("删除过期代理IP："+ip+"失败")
        self.db.commit()

    def test_connection(self,protocol,ip,port):
        """
        检测代理的有效性
        :param protocol:
        :param ip:
        :param port:
        :return:
        """
        #logging.basicConfig(level=logging.NOTSET)  # 设置日志级别
        #proxies = {protocol: ip + ":" + port}
        proxies = protocol+"://"+ip + ":" + port
        proxy={"http":proxies}
        try:
           # OrigionalIP = requests.get("http://icanhazip.com", timeout=REQ_TIMEOUT).content
            MaskedIP = requests.get("http://icanhazip.com", timeout=3, proxies=proxy).content
            if MaskedIP!=None:
                print(MaskedIP)
                logging.debug("代理"+proxies+"可用")
                return True
            else:
                print(MaskedIP)
                print("代理"+proxies+"不可用")
                return False
        except:
            return False
    
    def test_connection_1(self,proxies):
        """
        检测代理的有效性
        :param protocol:
        :param ip:
        :param port:
        :return:
        """
        logging.basicConfig(level=logging.NOTSET)  # 设置日志级别
        #proxies = {protocol: ip + ":" + port}
        proxy={"http":proxies}
        try:
           # OrigionalIP = requests.get("http://icanhazip.com", timeout=REQ_TIMEOUT).content
            MaskedIP = requests.get("http://icanhazip.com", timeout=3, proxies=proxy).content
            if MaskedIP!=None:
                logging.debug("代理"+proxies+"可用")
                return True
            else:
                logging.debug("代理"+proxies+"不可用")
                return False
        except:
            return False

    def Is_Empty(self):
        """
        查询数据库表kuaidaili是否为空
        """
        sql="select count(*) from kuaidaili;"
        self.cur.execute(sql)
        result=self.cur.fetchone()
        self.db.commit()
        count=result[0]
        if count==0:
            return True
        else:
            return False

    def clean_nonworking(self):
        """
        循环代理池，逐行测试IP地址端口协议是否可用
        :return:
        """
        sql="select * from kuaidaili;"
        self.cur.execute(sql)
        all=self.cur.fetchall()
        self.db.commit()
        if not all==None:
          for line in all:
            protocol=line[3]
            ip=line[0]
            port=line[1]
            isAnonymous=self.test_connection(protocol,ip,port)
            if isAnonymous==False:
                print('delete outdate proxy:'+ip)
                self.del_record(ip)


    def pop_one(self):
        """
        取出表中第一条记录
        """
        sql="select * from kuaidaili limit 1;"
        self.cur.execute(sql)
        line=self.cur.fetchone()
        self.db.commit()
        protocol=line[3]
        ip=line[0]
        port=line[1]
        proxies = protocol+"://"+ip + ":" + port
        return ip,proxies

    def pop_all(self):
        """
        取出表中所有记录
        """
        sql="select * from kuaidaili;"
        self.cur.execute(sql)
        ips=self.cur.fetchall()
        self.db.commit()
        proxies=[]
        for line in ips:
            protocol=line[3]
            ip=line[0]
            port=line[1]
            proxy = protocol+"://"+ip + ":" + port
            proxies.append(proxy)
        return ips,proxies


if __name__=="__main__":
    import KuaiDaiLiIp_Spider
    s=Proxy_Pool()
    d=KuaiDaiLiIp_Spider.KuaiDaiLiIp_Spider()
    url='http://www.kuaidaili.com/free/inha/'
    for i in range(1,30):
       s.add_proxy(d.ParseAndGetInfo(url,i))
    # if not s.Is_Empty():
    #     ip,proxies=s.pop_one()
    #     if s.test_connection_1(proxies):
    #         print("代理可用")
    #         #s.del_record(ip)
    #     else:
    #         print("代理不可用")
    #         s.del_record(ip)
    s.clean_nonworking()
    del s
        
