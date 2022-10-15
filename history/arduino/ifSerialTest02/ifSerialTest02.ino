#include <SoftwareSerial.h>
#include<LiquidCrystal_I2C.h>
#include<Wire.h>

LiquidCrystal_I2C lcd(0x3F,16,2); //LCD 클래스 초기화

char cmd;
int cmdvalue;
int cnt=0;
int allnum[7];
char cmd_h;
boolean state=false;
boolean errorstate=false;
const unsigned long TimeOut = 10;

byte giyuk[] = {
  B00000,
  B11111,
  B00001,
  B00001,
  B00001,
  B00001,
  B00001,
  B00000
};

byte nieun[] = {
  B00000,
  B10000,
  B10000,
  B10000,
  B10000,
  B10000,
  B11111,
  B00000
};

byte ah[] = {
  B00100,
  B00100,
  B00100,
  B00111,
  B00100,
  B00100,
  B00100,
  B00100
};

void setup() {
  // 시리얼 통신 시작 (boadrate: 9600)
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.print("Hello!");
  lcd.createChar(0,giyuk);
  lcd.createChar(1,nieun);
  lcd.createChar(2,ah);
}

void loop() {

  check();
  //wtf();
  if(state==true){
    lcdprint();
    state=false;   
  }else if(errorstate==true){
    errorlcdprint();
    errorstate=false;
  }

}

void check(){
  do
  {
    if(cnt==7){
      break;
    }
    if(Serial.available()){
      cmd = Serial.read();
      if(cmd=='e'){
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
        allnum[cnt]=cmdvalue;
        cnt++;
        Serial.println(cmdvalue);
        delay(100);
      }
    }
  }while(cmd!='!');
  cnt=0;
  state=true;
}

void lcdprint(){
  lcd.clear();
  for(int i=0;i<=2;i++)
  {
    lcd.setCursor(i,0);
    lcd.print(allnum[i]);
  }
  if(cmd_h=='a'){  
    lcd.setCursor(3,0);
    lcd.write(0);
    lcd.setCursor(4,0);
    lcd.write(2);
  }else if(cmd_h=='n'){
    lcd.setCursor(3,0);
    lcd.write(1);
    lcd.setCursor(4,0);
    lcd.write(1);
  }
  lcd.setCursor(5,0); 
  int j=3;
  for(int i=5;i<=8;i++)
  {
    lcd.setCursor(i,0);
    lcd.print(allnum[j]);
    j++;
  }
  lcd.setCursor(0,1);
  lcd.print("Welcome!");
}

void errorlcdprint(){
  lcd.clear();
  lcd.print("wait...");
}
//void wtf() {
//  int first[3] = {1,2,3};
//  for(int i=0;i<=2;i++)
//  {
//    lcd.setCursor(i,0);
//    lcd.print(first[i]);
//  }
//
//  lcd.printHangul(L"가",3,1);
//  lcd.setCursor(5,0); 
//  int second[4] = {4,5,6,7};
//  int j=0;
//  for(int i=5;i<=8;i++)
//  {
//    lcd.setCursor(i,0);
//    lcd.print(second[j]);
//    j++;
//  }
//  lcd.setCursor(0,1);
//  lcd.print("Welcome!");
//}
