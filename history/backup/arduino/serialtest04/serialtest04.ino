char cmd;
int cmdvalue;
int allnum[7]={};
char cmd_h;
boolean state=false;
void setup() {
  // 시리얼 통신 시작 (boadrate: 9600)
  Serial.begin(9600);
}

void loop() {
  check();
  if(state==true)
  {
    check2();
  }
}

void check(){
  for(int i=0;i<7;i++){
    if(Serial.available()){
      cmd = Serial.read(); 
      if(cmd=='1'){
        Serial.println("1 입력 받음 ㅋㅋ");
        cmdvalue=cmd-'0';
        allnum[0]=cmdvalue;
        delay(1000);
      }
      else if(cmd=='2'){
        Serial.println("2 입력 받음 ㅋㅋ" );
        cmdvalue=cmd-'0';
        allnum[1]=cmdvalue;
        delay(100);
      }
      else if(cmd=='3'){
        Serial.println("3 입력 받음 ㅋㅋ");
        cmdvalue=cmd-'0';
        allnum[2]=cmdvalue;
        delay(100);
      }
      else if(cmd=='4'){
        Serial.println("4 입력 받음 ㅋㅋ");
        cmdvalue=cmd-'0';
        allnum[3]=cmdvalue;
        delay(100);
      }
      else if(cmd=='5'){
        Serial.println("5 입력 받음 ㅋㅋ");
        cmdvalue=cmd-'0';
        allnum[4]=cmdvalue;
        delay(100);
      }
      else if(cmd=='6'){
        Serial.println("6 입력 받음 ㅋㅋ");
        cmdvalue=cmd-'0';
        allnum[5]=cmdvalue;
        delay(100);
      }
      else if(cmd=='7'){
        Serial.println("7 입력 받음 ㅋㅋ");
        cmdvalue=cmd-'0';
        allnum[6]=cmdvalue;
        delay(100);
      }
      else if(cmd=='a'){
        Serial.println("가 입력 받음 ㅋㅋ");
        cmd_h=cmd;
        delay(100);
        state=true;
      }
    }
  }
}

void check2(){
  for(int i=0;i<7;i++)
  {
    Serial.println(allnum[i]);
  }
  Serial.println(cmd_h);
  state=false;
}
