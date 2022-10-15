str = "123가4567" #문자열
char_list = list(str) #한글자씩 배열
Trans=str.encode('utf-8') #변환

hanguel = char_list.pop(3)# 빼내기
print(hanguel)

if hanguel == "가":
    hanguel_change = 'a'
print(hanguel_change)
print(char_list)

for i in char_list:
    print(i)