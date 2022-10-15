//우노 A4 A5 나르도 2 3

#include<LiquidCrystal_I2C_Hangul.h>
#include<Wire.h>

LiquidCrystal_I2C_Hangul lcd(0x3F,16,2); //LCD 클래스 초기화

char cmd_h='n';
int displaymenu=0;
void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  lcd.clear();
}

void loop() {

}
