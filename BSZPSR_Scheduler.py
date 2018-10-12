import pymysql
import BossZPRequestion_Spider
import PushData2MySql

def getDataList(db,cur,begin,end):
    sql_select = """select  `jid`,`lid` from `bszp_1` where `id` between {begin} and {end};""".format(begin=begin,end=end)
    cur.execute(sql_select)
    param_list = cur.fetchall()
    db.commit()
    data_list = []
    count=begin
    for line in param_list:
        try:
           print("开始爬取:"+line[0])
           spider = BossZPRequestion_Spider.BossZP_RequestionSpider(line[0], line[1])
           data_list.append(spider.main())
           count+=1
        except:
           print("spider" + str(count) + "get problem")
           count += 1
           pass
        finally:
           count += 1
    return data_list

# def insertDataList(db,cur,data_list)
#     illegalValues = []
#     #批量插入数据
#     if len(data_list) <= 0:
#         return
#     for key in data_list:
#            ls = list(key.values())
#            try:
#                cur.execute("""insert into `bszp_2`(`jid`,`job_requestion`) values(%s,%s);""", ls)
#            except:
#                illegalValues.append(key)
#                print(ip_list.index(key))
#                pass
#     db.commit()

def main():
    db = pymysql.connect(host='localhost', user='root', passwd='')
    cur = db.cursor()
    cur.execute('use maoyan;')
    sql = """select count(*) from `bszp_1`;"""
    cur.execute(sql)
    count = (cur.fetchone())[0]
    begin = 0
    end = 0

    """
    每20条记录插入一次数据库
    """
    while end <= count:
        end += 1
        if end%20==0 or end==count:
           ls=getDataList(db, cur, begin, end)
           PushData2MySql.pushData_2(db,cur,ls)
           begin = end + 1
    
    cur.close()
    db.close()

if __name__ == "__main__":
    main()
