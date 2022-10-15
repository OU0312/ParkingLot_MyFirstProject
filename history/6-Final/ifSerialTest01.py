import serial
import time
import threading

def charToArduino():
    hanguel_list_all = ["가","기","나","니","다","디","라","리","마","미","먀","므","바","비","뱌","브","사","시","샤","스","아","이","야","으","어","여","자","지","쟈","즈","하","히","햐","흐"]
    hanguel_list_ga = ["가","기","갸","그"]
    hanguel_list_na = ["나","니","냐","느"]
    hanguel_list_da = ["다","디","댜","드"]
    hanguel_list_ra = ["라","리","랴","르"]
    hanguel_list_ma = ["마","미","먀","므"]
    hanguel_list_ba = ["바","비","뱌","브"]
    hanguel_list_sa = ["사","시","샤","스"]
    hanguel_list_ah = ["아","이","야","으"]
    hanguel_list_ah2 = ["어","여"]
    hanguel_list_ja = ["자","지","쟈","즈"]
    hanguel_list_ha = ["하","히","햐","흐"]
    number_list = ['1','2','3','4','5','6','7','8','9','0']
    
    errorlog='e' # 에러 시리얼
    errorstate=False
    str = "갋789하12345" #문자열
    str_list = list(str) #한글자씩 배열
    hanguel = str_list.pop(3) #list에서 한글 빼기
    if hanguel not in hanguel_list_all :
        str_list.insert(3,hanguel)
        errorstate=True
    print(str_list)
    hanguel_change = ''
    #str_list_count = len(str_list)

    if hanguel not in hanguel_list_all: # 한글이 아닌 경우
        
        time.sleep(0.1)
        errorstate=True

    if hanguel in hanguel_list_ga and errorstate!=True:
        hanguel_change = "g"
        
        time.sleep(0.1)

    elif hanguel in hanguel_list_na and errorstate!=True:
        hanguel_change = "n"
        
        time.sleep(0.1)

    elif hanguel in hanguel_list_da and errorstate!=True:
        hanguel_change = "d"
        
        time.sleep(0.1)
    
    elif hanguel in hanguel_list_ra and errorstate!=True:
        hanguel_change = "r"
       
        time.sleep(0.1)
    
    elif hanguel in hanguel_list_ma and errorstate!=True:
        hanguel_change = "m"
        
        time.sleep(0.1)
        
    elif hanguel in hanguel_list_ba and errorstate!=True:
        hanguel_change = "b"
       
        time.sleep(0.1)
        
    elif hanguel in hanguel_list_sa and errorstate!=True:
        hanguel_change = "s"
        
        time.sleep(0.1)
        
    elif hanguel in hanguel_list_ah and errorstate!=True:
        hanguel_change = "a"
        
        time.sleep(0.1)
    
    elif hanguel in hanguel_list_ah2 and errorstate!=True:
        hanguel_change = "o"
        
        time.sleep(0.1)
        
    elif hanguel in hanguel_list_ja and errorstate!=True:
        hanguel_change = "j"
        
        time.sleep(0.1)
        
    elif hanguel in hanguel_list_ha and errorstate!=True:
        hanguel_change = "h"
        
        time.sleep(0.1)
        
    if str_list[0] not in number_list and errorstate==True:
        str_list.pop(0)


    if str_list[0] == '1' and errorstate==True:
        if str_list[1] == '2' :
            if str_list[2] == '3' :
                hanguel_change = "g"
                
                time.sleep(0.1)
    
    elif str_list[0] == '2' and errorstate==True:
        if str_list[1] == '6' :
            if str_list[2] == '1' :
                hanguel_change = "n"
                
                time.sleep(0.1)
                
    elif str_list[0] == '3' and errorstate==True:
        if str_list[1] == '2' :
            if str_list[2] == '1' :
                hanguel_change = "d"
                
                time.sleep(0.1)
                
    elif str_list[0] == '4' and errorstate==True:
        if str_list[1] == '5' :
            if str_list[2] == '0' :
                hanguel_change = "r"
              
                time.sleep(0.1)
                
    elif str_list[0] == '5' and errorstate==True:
        if str_list[1] == '6' :
            if str_list[2] == '5' :
                hanguel_change = "m"
         
                time.sleep(0.1)
                
    elif str_list[0] == '9' and errorstate==True:
        if str_list[1] == '5' :
            if str_list[2] == '1' :
                hanguel_change = "b"
          
                time.sleep(0.1)
                
    elif str_list[0] == '7' and errorstate==True:
        if str_list[1] == '7' :
            if str_list[2] == '7' :
                hanguel_change = "s"
               
                time.sleep(0.1)
                
    elif str_list[0] == '6' and errorstate==True:
        if str_list[1] == '7' :
            if str_list[2] == '8' :
                hanguel_change = "a"
                
                time.sleep(0.1)
                
    if str_list[0] == '5' and errorstate==True:
        if str_list[1] == '7' :
            if str_list[2] == '0' :
                hanguel_change = "o"
                
                time.sleep(0.1)
    
    elif str_list[0] == '7' and errorstate==True:
        if str_list[1] == '8' :
            if str_list[2] == '9' :
                hanguel_change = "j"
                
                time.sleep(0.1)
                
    elif str_list[0] == '2' and errorstate==True:
        if str_list[1] == '3' :
            if str_list[2] == '4' :
                hanguel_change = "h"
                
                time.sleep(0.1)
    
    print(str_list[0],str_list[1],str_list[2])            
    print(hanguel_change)
    
                
charThread=threading.Thread(target=charToArduino)
charThread.start()