#include <Servo.h>
Servo servo;
int pos=0;
int isPin = 4;
int infrared_sensorPin = 2; // 적외선 센서 노랑. 보드 2번 핀 연결
boolean state=false;

void setup()
{
  servo.attach(9);
  
  pinMode (infrared_sensorPin, INPUT);
  pinMode (isPin, INPUT);
  /*Serial.begin (9600);
  Serial.println ("infrared sensor start!");
  Serial.println ();*/
}
void loop()
{
  
  int sensorDetect = digitalRead (infrared_sensorPin);
  int second = digitalRead(isPin);
  /*Serial.print ("infrared sensor state : ");
  Serial.println (sensorDetect);*/
 if ( sensorDetect == LOW && second == HIGH)
  {
      servo.write(90);
      delay(2000); 
      //servo.detach();
      state=true;  
  }
  else if(second == LOW && sensorDetect == HIGH)
  {
    servo.write(0);
    //servo.detach();
    state=false;

  }
  delay (100);
}
