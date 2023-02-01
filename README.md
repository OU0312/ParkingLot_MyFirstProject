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

### 만약 지금 다시 만든다면??

개발 날짜 : 2022 여름~가을

Readme 작성 날짜 : 2023 봄

- Firabase 데이터 베이스를 사용한다.
- 파이썬 자체 GUI보다는 Api를 받아서 React로 UI 개발
- 모바일 UI 화면 개발
