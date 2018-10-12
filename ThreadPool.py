from  concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor
from threading import currentThread
import os,time,random
import BossZP_Spider

def taskView(n):
    print('%s:%s is running'%(currentThread().getName(),os.getpid()))  #看到的pid都是一样的，因为线程是共享了一个进程
    time.sleep(random.randint(1,3))  #I/O密集型的，，一般用线程，用了进程耗时长
    return n**2
def BSZPS_ThreadPool():
    start = time.time()
    p = ThreadPoolExecutor(3) #线程池 #如果不给定值，默认cup*5
    cities = ["杭州", "上海", "深圳"]
    l = []
    for i in range(3):  #10个任务 # 线程池效率高了
        task=BossZP_Spider.BossZP_Spider()
        obj = p.submit(task.main(city=cities[i]), i)  #相当于apply_async异步方法
        taskView(i)
        time.sleep(5)
        l.append(obj)
    p.shutdown()  #默认有个参数wite=True (相当于close和join)
    print('='*30)
    print([obj.result() for obj in l])
    print(time.time() - start)  #3.001171827316284

if __name__ == "__main__":
    BSZPS_ThreadPool()

