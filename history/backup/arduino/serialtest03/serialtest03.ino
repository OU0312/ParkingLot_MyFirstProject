char cmd;

void setup() {
  
  // 시리얼 통신 시작 (boadrate: 9600)
  Serial.begin(9600);
}

void loop() {

  // 컴퓨터로부터 시리얼 통신이 전송되면, 한줄씩 읽어와서 cmd 변수에 입력
  if(Serial.available()){
    cmd = Serial.read(); 

    if(cmd=='1'){
      Serial.println("1 입력 받음 ㅋㅋ");
      delay(1000);
    }
    else if(cmd=='2'){
      Serial.println("2 입력 받음 ㅋㅋ");
      delay(1000);
    }
    else if(cmd=='3'){
      Serial.println("3 입력 받음 ㅋㅋ");
      delay(1000);
    }
    else if(cmd=='4'){
      Serial.println("4 입력 받음 ㅋㅋ");
      delay(1000);
    }
    else if(cmd=='5'){
      Serial.println("5 입력 받음 ㅋㅋ");
      delay(1000);
    }
    else if(cmd=='6'){
      Serial.println("6 입력 받음 ㅋㅋ");
      delay(1000);
    }
    else if(cmd=='7'){
      Serial.println("7 입력 받음 ㅋㅋ");
      delay(1000);
    }
  }
}
