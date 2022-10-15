import serial
import time

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
str = "123가4657" #문자열
str_list = list(str) #한글자씩 배열
hanguel = str_list.pop(3) #list에서 한글 빼기
if hanguel not in hanguel_list_all :
    str_list.insert(3,hanguel)
print(str_list)
if(str_list[0] in number_list) :
    print("숫자지롱")