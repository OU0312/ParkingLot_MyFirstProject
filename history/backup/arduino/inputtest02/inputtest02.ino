#include "Keyboard.h"

int infrared_sensorPin = 2; // 적외선 센서 노랑. 보드 2번 핀 연결
int isPin=3;
int Flag = 0;
int count = 0;
int excount = 1;

void setup()
{
  pinMode (infrared_sensorPin, INPUT);
  pinMode (isPin, INPUT);
  Keyboard.begin();
  attachInterrupt(digitalPinToInterrupt(isPin),ONCE,CHANGE);
}
void loop()
{
}

void ONCE()
{
  if(digitalRead(isPin)==LOW)
  {
    if(Flag==0)
    {
      Keyboard.write('o');
    delay(100);
    Keyboard.releaseAll();
    delay(100);
    }
    else{
      
    }
  }
  else{
    Flag=0;
  }
}
