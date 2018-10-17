#功能：动态更新IP
import os
import time
print(os.popen('rasdial /DISCONNECT').read())
time.sleep(3)
print(os.popen('rasdial "设定的宽带名称"  帐号 密码').read())
print(os.popen('rasdial').read())
time.sleep(1)
