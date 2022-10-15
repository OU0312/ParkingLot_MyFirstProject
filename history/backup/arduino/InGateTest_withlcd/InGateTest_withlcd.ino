#include <Servo.h>
#include "Keyboard.h"
#include <SoftwareSerial.h>
#include<LiquidCrystal_I2C_Hangul.h>
#include<Wire.h>

LiquidCrystal_I2C_Hangul lcd(0x3F,16,2); //LCD 클래스 초기화

// lcd with python
char cmd;
int cmdvalue;
int cnt=0;
int allnum[7];
char cmd_h;
int state=0;
const unsigned long TimeOut = 10;

//servo
int servoPin=13;
Servo servo;
int angle=0;

//sensor
int inSensor1=8;
int inSensor2=9;
int inSensor3=10;
int gatestate=HIGH;

void setup() {
  Keyboard.begin();
  servo.attach(servoPin);
  servo.write(110);
  Serial.begin (9600);
  Serial.println("test");
  
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.print("Hello!");
  
  pinMode (inSensor1, INPUT);
  pinMode (inSensor2, INPUT);
  pinMode (inSensor3, INPUT);

}

void loop() {
  sensorCheck();
  pythoncheck();
  lcdcheck();
}

void sensorCheck(){
  int inSensorDetect1 = digitalRead (inSensor1);
  int inSensorDetect2 = digitalRead (inSensor2);
  int inSensorDetect3 = digitalRead (inSensor3);
  if (inSensorDetect1 == LOW && inSensorDetect3 == HIGH)
  {
    Serial.println("1번센서 작동");
    servo.write(0);
    delay(2000);
    if(inSensorDetect2 == LOW)
    {
      Serial.println("2번센서 작동");
      Keyboard.write('i');
      Keyboard.releaseAll();
      delay(2000);
    }
  }
  else if(inSensorDetect3 == LOW)
  {
    //Serial.println("3번센서 작동");
    gatestate=LOW;
  }
  else if(gatestate==LOW && inSensorDetect1 == HIGH && inSensorDetect3 == HIGH)
  {
    servo.write(110);
    delay(2000);
    gatestate=HIGH;
  }
}

void lcdcheck(){
  switch(state){
    case 1:{
      lcdprint();
      cnt=0;
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
  lcd.print("wait...");
}
