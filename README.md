# OpenCV를 이용한 차량번호인식 무인 주차장 운영 시스템 🚗

![readme1](https://user-images.githubusercontent.com/113419018/216010294-80ed1df8-698b-4cf6-8f3f-e5d2322d1dbd.gif)
![readme2](https://user-images.githubusercontent.com/113419018/216010528-55cfb248-9942-401d-bc99-8e810d7c7fe0.gif)

#### 2022 부천대학교 캡스톤 디자인 우수상

<div align="center">
<h4>Stack</h4>
  <div align="center">
  	<img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=Python&logoColor=white" />
  <img src="https://img.shields.io/badge/C++-00599C?style=flat&logo=cplusplus&logoColor=white" />
</div>
</div>
<br>

### Introduce

개발환경

    Python , Arduino Leonardo

- <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=OpenCV&logoColor=white" /> 를 이용해 '번호판 영역'을 추출
- 추출한 '번호판 영역'은 Tesseract OCR을 이용하여 문자열 데이터로 추출
- 파이썬 내부에서 작은 DB를 만들어서 사용
- tkiner 를 이용하여 주차장 관리자를 위한 GUI 제공

<hr>

### Conclusions

- 소프트웨어 기술과 하드웨어 기술의 통합 능력 습득
- 사진의 글자를 인식해서 데이터로 가져오는건 쉽지 않은 일이다. (특히 한글) 테서렉트의 기본 한글 데이터가 아닌 자동차 번호판에만 사용되는 한글 데이터를 사용하였고 인식한 문자열 데이터를 파이썬 내부에서 한번 더 검수 하였다. (갸 => 가)
- 객체지향 코딩의 중요성을 깨달았다. 학교에서 배우던 자바의 객체지향 개념은 "왜" 필요한지 알려 하지 않았고 그저 코딩을 따라 칠 뿐이었다. 하지만 나의 작품을 주도적으로 더 효율적으로 만들기 위해 호기심으로 가득 차 있었던 나는 객체 지향의 개념을 각종 책과 유튜브로 습득하였고 그저 시켜서 하는 "외부 동기" 보다는 내가 직접 깨닫는 "내부 동기"의 중요성을 깨달았다.
- 처음으로 주도적으로 만들어본 작품이라 코딩의 퀄리티는 많이 부족할수있다. 그러나 주도적인 학습의 중요성을 알게 해준 작품이므로 내게는 가치가 큰 작품이다.

<hr>

### ⚙️ Update ⚙️

#### 번호판 인식 알고리즘 수정(23.02.21)

첫 프로젝트였던 만큼 알고리즘 짜는 실력이 많이 부족했기에 다시 짰습니다.

수정 전:

```python
hanguel_list_all = ["가","기","나","니","다","디","라","리","마","미","먀","므","바","비","뱌","브","사","시","샤","스","아","이","야","으","어","여","자","지","쟈","즈","하","히","햐","흐"]
hanguel_list_ga = ["가","기","갸","그"]
hanguel_list_na = ["나","니","냐","느"]
hanguel_list_da = ["다","디","댜","드"]
hanguel_list_ra = ["라","리","랴","르"]
hanguel_list_ma = ["마","미","먀"]
... #반복...

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
... #반복...
```

후:

```python
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

chars="123가4567"

errorlog='e' # 에러 시리얼
error_state=False
license_plate = list(chars) #한글자씩 배열
count = len(license_plate) #번호판 길이

#번호판이 너무 길다면
if count != 8:
    if license_plate[0:3] not in number_list:
            for i in license_plate[0:3]:
                index = license_plate.index(i)
                if i not in number_list:
                    print("found you",i)
                    license_plate.pop(license_plate.index(i))
    if license_plate[-4:] not in number_list:
        for i in license_plate[-4:]:
            index = license_plate.index(i)
            if i not in number_list:
                print("found you",i)
                license_plate.pop(license_plate.index(i))

hangeul = license_plate.pop(3) #list에서 한글 빼기
hangeul_key = "" # 한글 수정
hangeul_data_to_arduino = '' #아두이노 시리얼로 보낼 데이터

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
```

실행결과 :

```py
key : 가
serial : g
['1', '2', '3'] 가 ['4', '5', '6', '7']
```

오류 검출시 :

```py
#chars="123갸4567"

key : 가
serial : g
['1', '2', '3'] 가 ['4', '5', '6', '7']
```

```py
#chars="걃123가4567"

found you 걃
key : 가
serial : g
['1', '2', '3'] 가 ['4', '5', '6', '7']
```

```py
#chars="궯123갸4567걃"

found you 궯
found you 걃
key : 가
serial : g
['1', '2', '3'] 가 ['4', '5', '6', '7']
```

<hr>

### 만약 지금 다시 만든다면??

개발 날짜 : 2022 여름~가을

Readme 작성 날짜 : 2023 봄

- Firabase 데이터 베이스를 사용한다.
- 파이썬 자체 GUI보다는 Api를 받아서 React로 UI 개발
- 모바일 UI 화면 개발
