#include <Servo.h>
#include "Keyboard.h"

//servo
int servoPin=13;
Servo servo;
int angle=0;

//sensor
int inSensor1=8;
int inSensor2=9;
int inSensor3=10;
int state=HIGH;

void setup() {
  Keyboard.begin();
  servo.attach(servoPin);
  servo.write(110);
  Serial.begin (9600);
  Serial.println ("테스트 시작!");
  Serial.println ();

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
    Serial.println("3번센서 작동");
    state=LOW;
    delay(2000);
  }
  else if(state==LOW && inSensorDetect1 == HIGH && inSensorDetect3 == HIGH)
  {
    state=inSensorDetect3;
    servo.write(110);
    delay(2000);
    state=HIGH;
  }
}
