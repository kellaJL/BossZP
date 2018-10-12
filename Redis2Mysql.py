#!/usr/bin/env python
# coding=utf-8
 
# ����ȡ���Ĳ�Ʒ��Ϣ��redis���ݿ�浽mysql�ģ����ݿ�'��Ʒ��Ϣ��'��
import json
import redis
import pymysql
 
def main():
    # ָ��redis���ݿ���Ϣ
    rediscli = redis.StrictRedis(host='localhost',port=6379,db=0)
    # ָ��mysql���ݿ�
    mysqlcli = pymysql.connect(host="localhost",port=3306,user="root",passwd="jinlulu666",db="maoyan",charset="utf8")
    while True:
        # ��redis����ȡ���ݣ�FIFOģʽΪ blpop��LIFOģʽΪ brpop����ȡ��ֵ
        data = rediscli.lpop("bzp_lsit")
        # item = json.loads(data.decode("utf-8"))
        item = json.loads(data)
        try:
            # ʹ��cursor()������ȡ�����α�
            cursor = mysqlcli.cursor()
            sql = "insert into bzp(job_title,job_red,job_requestion,job_location,job_experience,e_b)VALUES(%s,%s,%s,%s,%s,%s) "
            cursor.execute(sql,[item['job_title'], item['job_red'], item['job_requestion'],
                item['job_location'], item['job_experience'], item['e_b']])
            mysqlcli.commit()
            cursor.close()
    
        except pymysql.Error as e:
            mysqlcli.rollback()
            print("�������ݴ���",e)
            # print("Mysql Error %d:%s"%(e.args[0],e.args[1]))
 
if __name__ == "__main__":
    main()
