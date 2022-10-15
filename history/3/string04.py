str = "123가4567" #문자열
str_list = list(str) #한글자씩 배열
hanguel = str_list.pop(3)
n=len(str_list)
if n!=7 :
    print("7 아님 ㅅㄱ")
print(n)
if hanguel == "가":
    hanguel_change = 'g'