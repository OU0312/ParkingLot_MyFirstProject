#include <Servo.h>
#include<SoftwareSerial.h>
#include<LiquidCrystal_I2C_Hangul.h>
#include<Wire.h>
#include "Keyboard.h"

//servo
int servoPin=13;
Servo servo;
int angle=0;

//sensor
int inSensor1=8;
int inSensor2=9;
int inSensor3=10;
int gatestate=HIGH;
int welcomeState=LOW;

//lcd with python
LiquidCrystal_I2C_Hangul lcd(0x3F,16,2); //LCD 클래스 초기화
char cmd;
int cmdvalue;
int cnt=0;
int allnum[7];
char cmd_h;
int lcdstate=0;
int seven=LOW;
int errorseven=LOW;

void setup() {
  Keyboard.begin();
  servo.attach(servoPin);
  servo.write(105);
  //Serial.begin (9600);
  Serial.println ("테스트 시작!");
  Serial.println ();
  lcd.init();
  lcd.backlight();
  lcd.clear();
  normalprint();
  
  pinMode (inSensor1, INPUT);
  pinMode (inSensor2, INPUT);
  pinMode (inSensor3, INPUT);

}

void loop() {
  sensorCheck();
}

void sensorCheck(){
  
  int inSensorDetect1 = digitalRead (inSensor1);
  int inSensorDetect2 = digitalRead (inSensor2);
  int inSensorDetect3 = digitalRead (inSensor3);
  if (inSensorDetect1 == LOW && inSensorDetect3 == HIGH && welcomeState == LOW)
  {
    Serial.begin (9600);
    Serial.println("1번센서 작동");
    lcdstate=2;
    lcdCheck();
    welcomeState=HIGH;
    delay(1000);
  }else if(inSensorDetect2 == LOW && welcomeState==HIGH){
    Serial.println("2번센서 작동");
    delay(2000);
    if(seven!=HIGH){
      Keyboard.write('i');
      Keyboard.releaseAll();
      delay(1000);
      pythonCheck();
    }else if(errorseven==HIGH){
      Keyboard.write('i');
      Keyboard.releaseAll();
      delay(1000);
      pythonCheck();
    }
    lcdCheck();
    delay(1000);
  }
  else if(inSensorDetect3 == LOW)
  {
    Serial.println("3번센서 작동");
    Keyboard.write('p');
    gatestate=LOW;
    delay(1000);
  }
  else if(gatestate==LOW && inSensorDetect1 == HIGH && inSensorDetect3 == HIGH && welcomeState==HIGH)
  {
    servo.write(105);
    delay(2000);
    gatestate=HIGH;
    welcomeState=LOW;
    seven=LOW;
    lcdstate=3;
    lcdCheck();
    delay(1000);
  }
}

void lcdCheck(){
  switch(lcdstate){
    case 1:{ // 번호판 출력
      seven=HIGH;
      Serial.end();
      errorseven=LOW;
      lcdprint();
      cnt=0;
      servo.write(0);
    }break;
    case 2:
    {
      comeslowprint();
    }break;
    case 3:
    {
      normalprint(); 
    }break;
    case 9:{ // 에러
      errorseven=HIGH;
      errorlcdprint();
    }break;
  }
}
void pythonCheck(){
  do
  {
    if(cnt==7 || errorseven==HIGH){     
      break;
    }
    if(Serial.available()){
      cmd = Serial.read();
      if(cmd=='e'){
        //Serial.println("다시 찍어야하니까 ㄱㄷ");
        errorseven=HIGH;
        lcdstate=9; // 9 error
        break;
      }
      else if(cmd=='a')
      {
        //Serial.println("가 입력 받음 ㅋㅋ");
        cmd_h=cmd;
        delay(100);
      }
      else if(cmd=='n')
      {
        //Serial.println("나 입력 받음 ㅋㅋ");
        cmd_h=cmd;
        delay(100);
      }
      else if(cmd=='d')
      {
        //Serial.println("다 입력 받음 ㅋㅋ");
        cmd_h=cmd;
        delay(100);
      }
      else
      {
        cmdvalue=cmd-'0';
        allnum[cnt]=cmdvalue;
        cnt++;
        //Serial.println(cmdvalue);
        delay(100);
      }
    }
  }while(cmd!='!');
  if(errorseven==HIGH)
  {
    lcdstate = 9;
  }
  else
  {
    lcdstate = 1; // default
  }
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

void comeslowprint(){
  lcd.clear();
  lcd.print("COME SLOW");
}

void normalprint(){
  lcd.clear();
  lcd.print("Time : ??-??-??");
  lcd.setCursor(0,1);
  lcd.print("Left : ??");
}
