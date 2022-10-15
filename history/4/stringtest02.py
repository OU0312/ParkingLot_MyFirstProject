number_list_all = ['1','2','3','4','5','6','7','8','9','0']


str = "123가4569" #문자열
str_list = list(str) #한글자씩 배열
hanguel = str_list.pop(3) #list에서 한글 빼기
print(str_list)
str_list_count = len(str_list)

for i in str_list:
    if i not in number_list_all:
        print("응 없어")