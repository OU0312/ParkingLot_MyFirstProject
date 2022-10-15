#include "Keyboard.h"

int infrared_sensorPin = 2; // 적외선 센서 노랑. 보드 2번 핀 연결
int isPin=3;


void setup()
{
  pinMode (infrared_sensorPin, INPUT);
  pinMode (isPin, INPUT);
  Keyboard.begin();
}
void loop()
{
  
  int sensorDetect = digitalRead (infrared_sensorPin);
  int sD = digitalRead (isPin);
  if ( sensorDetect == LOW)
  {
    Keyboard.write('i');
    Keyboard.releaseAll();
    delay(2000);
  }else if(sD == LOW)
  {
    Keyboard.write('o');
    delay(100);
    Keyboard.releaseAll();
    delay(100);
  }
  
}
