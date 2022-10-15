char cmd;
int cmdvalue;
int allnum[]={};
char cmd_h;
boolean state=false;
const unsigned long TimeOut = 10;

void setup() {
  // 시리얼 통신 시작 (boadrate: 9600)
  Serial.begin(9600);

}

void loop() {
//  unsigned long T = 0;
//  T =millis();
//  while (millis() - T < TimeOut) {
//    // waiting timeout
//    while (Serial.available() > 0) {
//      // receiving Serial
//      check4();
//      T = millis(); // reset timer
//    }
//  }
  check4();
}

void check4(){
  if(Serial.available()){
    int i=0;
      cmd = Serial.read();
      if(cmd=='a'){
        Serial.println("어 입력 받음 ㅋㅋ");
        cmd_h=cmd;
        delay(100);
      }else{
        cmdvalue=cmd-'0';
        allnum[i]=cmd;
        i++;
        Serial.println(cmdvalue);
        delay(100);
      }
  }
}
