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
      pythonCheckFake();
    }else if(errorseven==HIGH){
      Keyboard.write('i');
      Keyboard.releaseAll();
      delay(1000);
      pythonCheckFake();
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
      errorseven=LOW;
      lcdprint();
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

void pythonCheckFake(){
  if(Serial.available()){
    cmd=Serial.read();
    if(cmd=='e'){
      lcdstate=9; // 9 error
    }
    else if(cmd=='g' || cmd=='n' || cmd=='d' || cmd=='r' || cmd=='m' || cmd=='b' || cmd=='s' || cmd=='a' || cmd=='o' || cmd=='j' || cmd=='h' )
    {
      cmd_h=cmd;
      lcdstate=1;
      delay(100);
    }
  }
}

void lcdprint(){
  lcd.clear();
  if(cmd_h=='a'){ 
    lcd.print(123); 
    lcd.printHangul(L"가",3,1);
    lcd.setCursor(5,0);
    lcd.print(4567);
  }else if(cmd_h=='n'){
    lcd.print(261);
    lcd.printHangul(L"나",3,1);
    lcd.print(6752);
  }else if(cmd_h=='d'){
    lcd.print(321);
    lcd.printHangul(L"다",3,1);
    lcd.print(9981);
  }else if(cmd_h=='r'){
    lcd.print(450);
    lcd.printHangul(L"라",3,1);
    lcd.print(2512);
  }else if(cmd_h=='m'){
    lcd.print(565);
    lcd.printHangul(L"마",3,1);
    lcd.print(2547);
  }else if(cmd_h=='b'){
    lcd.print(951);
    lcd.printHangul(L"바",3,1);
    lcd.print(5452);
  }else if(cmd_h=='s'){
    lcd.print(777);
    lcd.printHangul(L"사",3,1);
    lcd.print(7777);
  }else if(cmd_h=='a'){
    lcd.print(678);
    lcd.printHangul(L"아",3,1);
    lcd.print(1229);
  }else if(cmd_h=='o'){
    lcd.print(570);
    lcd.printHangul(L"어",3,1);
    lcd.print(5971);
  }else if(cmd_h=='j'){
    lcd.print(789);
    lcd.printHangul(L"자",3,1);
    lcd.print(4123);
  }else if(cmd_h=='h'){
    lcd.print(234);
    lcd.printHangul(L"하",3,1);
    lcd.print(5678);
  }
  lcd.setCursor(0,1);
  lcd.print("Welcome!");
}

void errorlcdprint(){
  lcd.clear();
  lcd.print("ERROR!");
  lcd.setCursor(0,1);
  lcd.print("RETRY PLZ");
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
