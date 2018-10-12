
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------
#   程序：xicidaili.py
#   版本：0.1
#   作者：
#   日期：
#   语言：Python3.7
#   操作：
#   功能：从www.xicidaili.com网站采集代理信息并存入数据库
#-------------------------------------------------------------------------
import requests,re,json
import sys,os,time,pymysql

# --------------------------------------------------
# 中文编码设置

# sys.setdefaultencoding('utf-8')
# sys.
# Type = sys.getfilesystemencoding()

# 数据库设置
MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'maoyan'
MYSQL_USER = 'root'
MYSQL_PASSWD = ''
MYSQL_PORT= 3306

# 此处修改数据库插入修改语句
install_str = '''
INSERT INTO proxy_xici( `proxy_ip`, `proxy_port`, `proxy_country`, `proxy_type`, `addtime`, `Last_test_time`, `proxy_status`, `Remarks`   )
VALUES (%s,%s,%s,%s,%s,%s,%s,%s)  '''

# 此处修改伪造的头字段,
headers = {
    'Host':"www.xicidaili.com",#需要修改为当前网站主域名
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
	"referer" : '123.123.123.123'#随意的伪造值
}


# 执行插入操作,导入插入语句,插入的数据,和数据库连接
def insert_ll(install_str,address_ll,conn,cur):
    mysql_str = install_str
    try:
        conn.ping()
        print('ping ing ')
    except:
       
        conn = pymysql.connect(host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PASSWD,db=MYSQL_DBNAME,port=MYSQL_PORT,charset='utf8')
        cur = conn.cursor()
    #print self.mysql_str % address_ll
    try:
        cur.execute(mysql_str,address_ll)
    except:
       print("插入错误3")
    return None


#发起请求,
def get_request(url,headers):
    '''参数引入及头信息'''
    print(requests.get(url).status_code)
    html=requests.post(url).text
    
    return html


# 将页面源代码正则匹配并解析,返回列表,其中每一项是json的数据
def re_html_code(html_code,proxy_list_json):

    # re正则取出数据
    try:
        re_list_ip = re.findall(r'<td>\d*\.\d*\.\d*\.\d*</td>',html_code)
        re_list_port = re.findall(r'<td>[\d]*</td>',html_code)
        re_list_live_time = re.findall(u'<td>\d*[小时分钟天]+</td>',html_code)
        print(re_list_live_time)
        #print type(html_code),type(r'<td>\d*[小时分钟天]+</td>')
        re_list_time = re.findall(r'<td>\d*-\d*-\d* \d*:\d*</td>',html_code)
        #print re_list_ip
        l = len(re_list_ip)
        for i in range(l):
            PROXY_IP = re_list_ip[i].replace('<td>','').replace('</td>',"")
            PROXY_PORT = re_list_port[i].replace('<td>','').replace('</td>',"")
            PROXY_COUNTRY = 'China'
            PROXY_TYPE= 'Elite'
            addtime = re_list_time[i].replace('<td>','').replace('</td>',"")
            Last_test_time = re_list_live_time[i].replace('<td>','').replace('</td>',"")
            #print Last_test_time
            #time.sleep(10)
            proxy_status = '1'
            Remarks = 'ly'
            # `id`, `proxy_ip`, `proxy_port`, `proxy_country`, `proxy_type`, `addtime`, `Last_test_time`, `proxy_status`, `Remarks`
            list_i = [PROXY_IP,PROXY_PORT,PROXY_COUNTRY,PROXY_TYPE,addtime,Last_test_time,proxy_status,Remarks]

            proxy_list_json.append(list_i)

        print(proxy_list_json)
        return proxy_list_json

    except:
        print("插入错误4")
#{'PROXY_STATUS': 'OK', 'PROXY_CITY': '', 'PROXY_TIME': '548', 'PROXY_STATE': '', 'PROXY_REFS': '', 'PROXY_TYPE': 'Transparent', 'PROXY_COUNTRY': 'China', 'PROXY_LAST_UPDATE': '1 59', 'PROXY_UPTIMELD': '105/16', 'PROXY_UID': '', 'PROXY_PORT': '1F90', 'PROXY_IP': '61.158.173.14'}





if __name__ == '__main__':
    try:
        conn = pymysql.connect(host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PASSWD,db=MYSQL_DBNAME,port=MYSQL_PORT,charset='utf8')
        cur = conn.cursor()
    except:
        print("插入错误1")

    for i in range(1,2):
        url = "http://www.xicidaili.com/nn/"+str(i)
        print('begin:',url)
        try:
            #html_code = get_request(url,headers)
            html_code = get_request(url,headers)
            proxy_list_json = []
            now_url = url
            proxy_list_json = re_html_code(html_code,proxy_list_json)
            for i in proxy_list_json:
                insert_ll(install_str,i,conn,cur)
        except:
            print("插入错误2")
