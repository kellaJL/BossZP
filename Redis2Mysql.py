#!/usr/bin/env python
# coding=utf-8
 
# 将获取到的产品信息从redis数据库存到mysql的：数据库'产品信息表'中
import json
import redis
import pymysql
 
def main():
    # 指定redis数据库信息
    rediscli = redis.StrictRedis(host='localhost',port=6379,db=0)
    # 指定mysql数据库
    mysqlcli = pymysql.connect(host="localhost",port=3306,user="root",passwd="",db="maoyan",charset="utf8")
    while True:
        # 从redis里提取数据，FIFO模式为 blpop，LIFO模式为 brpop，获取键值
        data = rediscli.lpop("bzp_lsit")
        # item = json.loads(data.decode("utf-8"))
        item = json.loads(data)
        try:
            # 使用cursor()方法获取操作游标
            cursor = mysqlcli.cursor()
            sql = "insert into bzp(job_title,job_red,job_requestion,job_location,job_experience,e_b)VALUES(%s,%s,%s,%s,%s,%s) "
            cursor.execute(sql,[item['job_title'], item['job_red'], item['job_requestion'],
                item['job_location'], item['job_experience'], item['e_b']])
            mysqlcli.commit()
            cursor.close()
    
        except pymysql.Error as e:
            mysqlcli.rollback()
            print("插入数据错误",e)
            # print("Mysql Error %d:%s"%(e.args[0],e.args[1]))
 
if __name__ == "__main__":
    main()
