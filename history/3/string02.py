str = "123가4567" #문자열
list = list(str) #한글자씩 배열
n=len(list) #배열 길이
Trans=str.encode('utf-8') #변환

for i in list: #반복
    Trans=i.encode('utf-8') #변환
    print(Trans)