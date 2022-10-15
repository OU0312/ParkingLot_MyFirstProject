import serial
import time

#serial 선언
py_serial = serial.Serial(
    
    # Window port
    port='COM8',
    
    # 보드 레이트 (통신 속도)
    baudrate=9600,
    
    timeout=10
)

#한글 리스트
hanguel_list_all = ["가","기","나","다","어","7","4"] 
hanguel_list_ga = ["가","기","7","4"]
hanguel_list_na = ["나","니","4","4"]

errorlog='!' # 에러 시리얼
str = "570나5971" #문자열
str_list = list(str) #한글자씩 배열 
hanguel = str_list.pop(3) #list에서 한글 빼기
print(str_list)
if hanguel not in hanguel_list_all: # 한글이 아닌 경우
    py_serial.write(errorlog.encode('utf-8'))
    time.sleep(0.1)
    if py_serial.readable():
        # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
        # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
        response = py_serial.readline()
            
        # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
        print(response[:len(response)-1].decode())
elif hanguel in hanguel_list_ga:
    hanguel_change = "a"
    py_serial.write(hanguel_change.encode('utf-8'))
    if py_serial.readable():
        time.sleep(0.1)
     # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
    # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
    response = py_serial.readline()
            
    # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
    print(response[:len(response)-1].decode())
elif hanguel in hanguel_list_na:
    hanguel_change = "n"
    py_serial.write(hanguel_change.encode('utf-8'))
    if py_serial.readable():
        time.sleep(0.1)
     # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
    # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
    response = py_serial.readline()
            
    # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
    print(response[:len(response)-1].decode())
    
str_list_count = len(str_list)
if str_list_count != 7 :
    py_serial.write(errorlog.encode('utf-8'))
    time.sleep(0.1)
    if py_serial.readable():
        # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
        # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
        response = py_serial.readline()
            
        # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
        print(response[:len(response)-1].decode())
else :
    for i in str_list: #반복
        py_serial.write(i.encode('utf-8'))
        time.sleep(0.1)
        if py_serial.readable():
            # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
            # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
            response = py_serial.readline()
                
            # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
            print(response[:len(response)-1].decode())
            

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

str2 = "123가4567" #문자열
str_list2 = list(str2) #한글자씩 배열 
hanguel2 = str_list2.pop(3) #list에서 한글 빼기
print(str_list2)
if hanguel2 not in hanguel_list_all: # 한글이 아닌 경우
    py_serial.write(errorlog.encode('utf-8'))
    time.sleep(0.1)
    if py_serial.readable():
        # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
        # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
        response = py_serial.readline()
            
        # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
        print(response[:len(response)-1].decode())
elif hanguel2 in hanguel_list_ga:
    hanguel_change2 = "a"
    py_serial.write(hanguel_change2.encode('utf-8'))
    if py_serial.readable():
        time.sleep(0.1)
        # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
        # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
        response = py_serial.readline()
                
        # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
        print(response[:len(response)-1].decode())
elif hanguel2 in hanguel_list_na:
    hanguel_change2 = "n"
    py_serial.write(hanguel_change2.encode('utf-8'))
    if py_serial.readable():
        time.sleep(0.1)
     # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
    # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
    response = py_serial.readline()
            
    # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
    print(response[:len(response)-1].decode())
    
str_list_count2 = len(str_list2)
if str_list_count2 != 7 :
    py_serial.write(errorlog.encode('utf-8'))
    time.sleep(0.1)
    if py_serial.readable():
        # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
        # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
        response = py_serial.readline()
            
        # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
        print(response[:len(response)-1].decode())
else :
    for i in str_list2: #반복
        py_serial.write(i.encode('utf-8'))
        time.sleep(0.1)
        if py_serial.readable():
            # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
            # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
            response = py_serial.readline()
                
            # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
            print(response[:len(response)-1].decode())
            
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# while True:
#     showme="*"
#     if py_serial.readable():
#         py_serial.write(showme.encode('utf-8'))
#         time.sleep(0.1)
#         # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
#         # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
#         response = py_serial.readline()
                
#         # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
#         print(response[:len(response)-1].decode())