import serial
import time

from sqlalchemy import false, true

#serial 선언
py_serial = serial.Serial(
    
    # Window port
    port='COM15',
    
    # 보드 레이트 (통신 속도)
    baudrate=9600,
    
    timeout=10
)

#한글 리스트
hanguel_list_all = ["가","기","나","니","다","디"] 
hanguel_list_ga = ["가","기"]
hanguel_list_na = ["나","니"]
hanguel_list_da = ["다","디"]
number_list_all = ['1','2','3','4','5','6','7','8','9','0']

errorlog='e' # 에러 시리얼
errorstate=False
str = "177가4569" #문자열
str_list = list(str) #한글자씩 배열
hanguel = str_list.pop(3) #list에서 한글 빼기
print(str_list)
str_list_count = len(str_list)

for i in str_list:
    if i not in number_list_all :
        py_serial.write(errorlog.encode('utf-8'))
        time.sleep(0.1)
        errorstate=True
    
if hanguel not in hanguel_list_all or errorstate==True: # 한글이 아닌 경우
    py_serial.write(errorlog.encode('utf-8'))
    time.sleep(0.1)
    errorstate=True
    if py_serial.readable():
        # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
        # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
        response = py_serial.readline()
            
        # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
        print(response[:len(response)-1].decode())
elif hanguel in hanguel_list_ga and errorstate!=True:
    hanguel_change = "a"
    py_serial.write(hanguel_change.encode('utf-8'))
    if py_serial.readable():
        time.sleep(0.1)
     # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
    # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
    response = py_serial.readline()
            
    # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
    print(response[:len(response)-1].decode())
elif hanguel in hanguel_list_na and errorstate!=True:
    hanguel_change = "n"
    py_serial.write(hanguel_change.encode('utf-8'))
    if py_serial.readable():
        time.sleep(0.1)
     # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
    # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
    response = py_serial.readline()
            
    # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
    print(response[:len(response)-1].decode())
elif hanguel in hanguel_list_da and errorstate!=True:
    hanguel_change = "d"
    py_serial.write(hanguel_change.encode('utf-8'))
    if py_serial.readable():
        time.sleep(0.1)
     # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
    # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
    response = py_serial.readline()
            
    # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
    print(response[:len(response)-1].decode())

if str_list_count != 7 or errorstate==True:
    py_serial.write(errorlog.encode('utf-8'))
    time.sleep(0.1)
    if py_serial.readable():
        # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
        # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
        response = py_serial.readline()
            
        # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
        print(response[:len(response)-1].decode())
elif str_list_count == 7 and errorstate!=True :
    for i in str_list: #반복p
        py_serial.write(i.encode('utf-8'))
        time.sleep(0.1)
        if py_serial.readable():
            # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
            # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
            response = py_serial.readline()
                
            # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
            print(response[:len(response)-1].decode())
            

    
