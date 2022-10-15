#include <DS1302.h>

#define SCK_PIN 5
#define IO_PIN 6
#define RESET_PIN 7

DS1302 myDS1302(7, 6, 5);

void setup(){
  myDS1302.halt(false);
  myDS1302.writeProtect(false);
  myDS1302.setDOW(FRIDAY);
  myDS1302.setDate(22,8,2022);
  myDS1302.setTime(16,33,00);
  Serial.begin(9600);
  while(!Serial){;}
  delay(500);
  Serial.println("Serial Port Connected..");
}

void loop(){
  Serial.print("@Date > ");
  Serial.print(myDS1302.getDOWStr());
  Serial.print(",");
  Serial.print(myDS1302.getDateStr(2,1,'-'));
  Serial.print("@Time > ");
  Serial.print(myDS1302.getTimeStr());
  Serial.println("");
  delay(1000);
}
