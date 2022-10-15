import serial
import time

py_serial = serial.Serial(
    
    # Window port
    port='COM8',
    
    # 보드 레이트 (통신 속도)
    baudrate=9600,
)

while True:
    str = "123가4567" #문자열
    str_list = list(str) #한글자씩 배열
    hanguel = str_list.pop(3)
    #n=len(list) 배열 길이

    for i in str_list: #반복
        py_serial.write(i.encode('utf-8'))
        time.sleep(0.1)
        if py_serial.readable():
            # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
            # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
            response = py_serial.readline()
            
            # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
            print(response[:len(response)-1].decode())
    
    
    
