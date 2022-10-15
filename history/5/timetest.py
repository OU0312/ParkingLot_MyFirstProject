import time
import threading

def sendtime():
    while True:
        hello=time.ctime()
        print(hello)
        str_list=list(hello)
        print(str_list)
        hour1=str_list.pop(11)
        hour2=str_list.pop(11)
        min1=str_list.pop(12)
        min2=str_list.pop(12)
        print(hour1)
        print(hour2)
        print(min1)
        print(min2)
        time.sleep(60)
        
sendtimeth=threading.Thread(target=sendtime)
sendtimeth.start()
while True:
    print("hello")
    time.sleep(1)