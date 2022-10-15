#include <SoftwareSerial.h>
#include<LiquidCrystal_I2C_Hangul.h>
#include<Wire.h>

LiquidCrystal_I2C_Hangul lcd(0x3F,16,2); //LCD 클래스 초기화

char cmd;
int cmdvalue;
int cnt=0;
int allnum[7];
char cmd_h;
int state=0;
const unsigned long TimeOut = 10;

void setup() {
  // 시리얼 통신 시작 (boadrate: 9600)
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.print("Hello!");
}

void loop() {
  pythoncheck();
  lcdcheck();
}

void lcdcheck(){
  switch(state){
    case 1:{
      lcdprint();
      cnt=0;
    }break;
    case 2:{
      slowprint();
    }break;
    case 9:{
      errorlcdprint();
    }break;
  }
}
void pythoncheck(){
  do
  {
    if(cnt>=7){
      state = 1; // normal
      break;
    }
    if(Serial.available()){
      cmd = Serial.read();
      if(cmd=='e'){
        Serial.println("다시 찍어야하니까 ㄱㄷ");
        state=9; // 9 error
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
      else if(cmd=='d')
      {
        Serial.println("다 입력 받음 ㅋㅋ");
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
}

void lcdprint(){
  lcd.clear();
  for(int i=0;i<=2;i++)
  {
    lcd.setCursor(i,0);
    lcd.print(allnum[i]);
  }
  if(cmd_h=='a'){  
    lcd.printHangul(L"가",3,1);
  }else if(cmd_h=='n'){
    lcd.printHangul(L"나",3,1);
  }else if(cmd_h=='d'){
    lcd.printHangul(L"다",3,1);
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
  lcd.print("ERROR!");
}

void slowprint(){
  lcd.clear();
  lcd.print("COME SLOW");
}

void defualtprint(){
  lcd.clear();
  lcd.print("Time : ??-??-??");
  lcd.setCursor(0,1);
  lcd.print("Left : ??");
}
