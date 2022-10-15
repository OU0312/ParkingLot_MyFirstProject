char cmd;
int cmdvalue;
int cnt;
int allnum[]={};
char cmd_h;
boolean state=false;
const unsigned long TimeOut = 10;

void setup() {
  // 시리얼 통신 시작 (boadrate: 9600)
  Serial.begin(9600);

}

void loop() {
  check();
  show();
}

void check(){
  do
  {
    if(Serial.available()){
      cnt=0;
      cmd = Serial.read();
      if(cmd=='!'){
        Serial.println("다시 찍어야하니까 ㄱㄷ");
        break;
      }
      else if(cmd=='a')
      {
        Serial.println("가 입력 받음 ㅋㅋ");
        cmd_h=cmd;
        delay(100);
      }
      else if(cmd=='n')
      {
        Serial.println("나 입력 받음 ㅋㅋ");
        cmd_h=cmd;
        delay(100);
      }
      else
      {
        cmdvalue=cmd-'0';
        allnum[cnt]=cmd;
        cnt++;
        Serial.println(cmdvalue);
        delay(100);
      }
    }
  }
  while(cmd!='!' || cnt<=7);
}

void show(){
  for(int i=0;i<7;i++)
  {
    Serial.println(allnum[i]);
  }
}
