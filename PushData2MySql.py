import pymysql



def pushData_1(data_list):
    db = pymysql.connect(host='localhost', user='root', passwd='')
    cur =db.cursor()
    cur.execute('use maoyan;')
    illegalValues=[]
               
    #批量插入数据
    for key in data_list:
        ls=list(key.values())
        try:
            cur.execute("""insert into `bszp_1`(`jid`,`lid`,`job_title`,`job_red`,`job_loaction`,`job_experience`,`e_b`) values(%s,%s,%s,%s,%s,%s,%s);""", ls)
               
        except:
            illegalValues.append(key)
            print(data_list.index(key))
            pass
    db.commit()
    cur.close()
    db.close()


def pushData_2(db,cur,data_list):
   
    illegalValues=[]
               
    #批量插入数据
    for key in data_list:
        ls=list(key.values())
        try:
            cur.execute("""insert into `bszp_2`(`jid`,`job_requestion`) values(%s,%s);""", ls)
               
        except:
            illegalValues.append(key)
            print(data_list.index(key))
            pass
    db.commit()
