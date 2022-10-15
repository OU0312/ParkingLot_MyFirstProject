char cmd;

void setup() {
  
  // 시리얼 통신 시작 (boadrate: 9600)
  Serial.begin(9600);
  pinMode(7,OUTPUT);
}

void loop() {

  // 컴퓨터로부터 시리얼 통신이 전송되면, 한줄씩 읽어와서 cmd 변수에 입력
  if(Serial.available()){
    cmd = Serial.read(); 

    if(cmd=='a'){
      Serial.println("a 입력 받음 ㅋㅋ");
      digitalWrite(7,HIGH);
      delay(100);
    }
    else if(cmd=='b'){
      Serial.println("b 입력 받음 ㅋㅋ");
      digitalWrite(7,LOW);
      delay(100);
    }
  }
}
