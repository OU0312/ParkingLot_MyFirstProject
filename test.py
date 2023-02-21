
number_list = ['1','2','3','4','5','6','7','8','9','0']
hangeul_list = {
    #key : [values,serial]
    "가" : ["가","기","갸","그",'g'],
    "나" : ["나","니","냐","느",'n'],
    "다" : ["다","디","댜","드",'d'],
    "라" : ["라","리","랴","르",'r'],
    "마" : ["마","미","먀",'m'],
    "바" : ["바","비","뱌","브",'b'],
    "사" : ["사","시","샤","스",'s'],
    "아" : ["아","이","야","으",'a'],
    "어" : ["어","여",'o'],
    "자" : ["자","지","쟈","즈",'j'],
    "하" : ["하","히","햐","흐",'h'],
}

chars="123갸4567"

errorlog='e' # 에러 시리얼
error_state=False
license_plate = list(chars) #한글자씩 배열
count = len(license_plate)

if count != 8:
    if license_plate[0:3] not in number_list:
            for i in license_plate[0:3]:
                index = license_plate.index(i)
                if i not in number_list:
                    print("found you",i)
                    license_plate.pop(index)
    if license_plate[-4:] not in number_list:
        for i in license_plate[-4:]:
            index = license_plate.index(i)
            if i not in number_list:
                print("found you",i)
                license_plate.pop(index)                
                
hangeul = license_plate.pop(3) #list에서 한글 빼기
hangeul_key = ""
hangeul_data_to_arduino = ''

for key,values in hangeul_list.items():
    if hangeul in values:
        error_state=False
        hangeul_key = key
        hangeul_data_to_arduino = values[-1]
        break
    else:
        error_state=True

if error_state == True:
    print("serial :",errorlog)
else:
    print("key :",hangeul_key,"\nserial :",hangeul_data_to_arduino)
    print(license_plate[0:3],hangeul_key,license_plate[-4:])



def charToArduino(camstate,chars):
    hanguel_list_ga = ["가","기","갸","그"]
    hanguel_list_na = ["나","니","냐","느"]
    hanguel_list_da = ["다","디","댜","드"]
    hanguel_list_ra = ["라","리","랴","르"]
    hanguel_list_ma = ["마","미","먀"]
    hanguel_list_ba = ["바","비","뱌","브"]
    hanguel_list_sa = ["사","시","샤","스"]
    hanguel_list_ah = ["아","이","야","으"]
    hanguel_list_ah2 = ["어","여"]
    hanguel_list_ja = ["자","지","쟈","즈"]
    hanguel_list_ha = ["하","히","햐","흐"]
    number_list = ['1','2','3','4','5','6','7','8','9','0']
    
    errorlog='e' # 에러 시리얼
    errorstate=False
    str = chars #문자열
    str_list = list(str) #한글자씩 배열
    hanguel = str_list.pop(3) #list에서 한글 빼기
    if hanguel not in hanguel_list_all :
        str_list.insert(3,hanguel)
        errorstate=True
    print(str_list)
    hanguel_change = ''
    #str_list_count = len(str_list)

    if hanguel not in hanguel_list_all: # 한글이 아닌 경우
        py_serial.write(errorlog.encode('utf-8'))
        time.sleep(0.1)
        errorstate=True

    if hanguel in hanguel_list_ga and errorstate!=True:
        hanguel_change = "g"
    
    elif hanguel in hanguel_list_na and errorstate!=True:
        hanguel_change = "n"

    elif hanguel in hanguel_list_da and errorstate!=True:
        hanguel_change = "d"
        
    elif hanguel in hanguel_list_ra and errorstate!=True:
        hanguel_change = "r"
        
    elif hanguel in hanguel_list_ma and errorstate!=True:
        hanguel_change = "m"
        
    elif hanguel in hanguel_list_ba and errorstate!=True:
        hanguel_change = "b"

    elif hanguel in hanguel_list_sa and errorstate!=True:
        hanguel_change = "s"

    elif hanguel in hanguel_list_ah and errorstate!=True:
        hanguel_change = "a"
        
    elif hanguel in hanguel_list_ah2 and errorstate!=True:
        hanguel_change = "o"

    elif hanguel in hanguel_list_ja and errorstate!=True:
        hanguel_change = "j"
        
    elif hanguel in hanguel_list_ha and errorstate!=True:
        hanguel_change = "h"
    
    if str_list[0] not in number_list and errorstate==True:
        str_list.pop(0)


    if str_list[0] == '1' and errorstate==True:
        if str_list[1] == '2' :
            if str_list[2] == '3' :
                hanguel_change = "g"
    
    elif str_list[0] == '2' and errorstate==True:
        if str_list[1] == '6' :
            if str_list[2] == '1' :
                hanguel_change = "n"
                
    elif str_list[0] == '3' and errorstate==True:
        if str_list[1] == '2' :
            if str_list[2] == '1' :
                hanguel_change = "d"
                
    elif str_list[0] == '4' and errorstate==True:
        if str_list[1] == '5' :
            if str_list[2] == '0' :
                hanguel_change = "r"
                
    elif str_list[0] == '5' and errorstate==True:
        if str_list[1] == '6' :
            if str_list[2] == '5' :
                hanguel_change = "m"
                
    elif str_list[0] == '9' and errorstate==True:
        if str_list[1] == '5' :
            if str_list[2] == '1' :
                hanguel_change = "b"
                
    elif str_list[0] == '7' and errorstate==True:
        if str_list[1] == '7' :
            if str_list[2] == '7' :
                hanguel_change = "s"
                
    elif str_list[0] == '6' and errorstate==True:
        if str_list[1] == '7' :
            if str_list[2] == '8' :
                hanguel_change = "a"
                
    if str_list[0] == '5' and errorstate==True:
        if str_list[1] == '7' :
            if str_list[2] == '0' :
                hanguel_change = "o"
    
    elif str_list[0] == '7' and errorstate==True:
        if str_list[1] == '8' :
            if str_list[2] == '9' :
                hanguel_change = "j"
                
    elif str_list[0] == '2' and errorstate==True:
        if str_list[1] == '3' :
            if str_list[2] == '4' :
                hanguel_change = "h"
    
    carnum = hangeul_to_carnum(hanguel_change)
    
    if camstate == "IN" :
        if hanguel_change not in db :
            db[hanguel_change] = hangeul_to_db(hanguel_change)
            print(carnum,"입차")
            py_serial.write(hanguel_change.encode('utf-8'))
            time.sleep(0.1)
            
    elif camstate == "OUT" :
        if hanguel_change in db :
            del(db[hanguel_change])
            print(carnum,"출차")
            py_serial.write(hanguel_change.encode('utf-8'))
            time.sleep(0.1)