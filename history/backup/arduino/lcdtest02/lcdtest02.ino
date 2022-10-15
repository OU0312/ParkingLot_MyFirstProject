//우노 A4 A5 레오나르도 2 3

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
  //lcd.print("Hello, world!");
//  lcd.setDelayTime(1000);
//  lcd.printHangul(L"한글출력입니다",0,7); //lcd.printHangul(한글 문장, 시작 포인트, 문장 길이);

}

void loop() {
  hard();
  delay(3000);
  displaymenu++;
  if(displaymenu>=4){
    displaymenu=0;
  }
}

void normal(){
      lcd.clear();
      int first[3] = {1,2,3};
      for(int i=0;i<=2;i++)
      {
        lcd.setCursor(i,0);
        lcd.print(first[i]);
      }
      if(cmd_h=='a'){  
        lcd.printHangul(L"가",3,1);
      }else if(cmd_h=='n'){
        lcd.printHangul(L"나",3,1);
      }
      lcd.setCursor(5,0); 
      int second[4] = {4,5,6,7};
      int j=0;
      for(int i=5;i<=8;i++)
      {
        lcd.setCursor(i,0);
        lcd.print(second[j]);
        j++;
      }
      lcd.setCursor(0,1);
      lcd.print("Welcome!");
}

void hard(){
  switch(displaymenu){
    case 0:{
      normal();
    }
    case 1:{
      normal();
    } break;
    case 2:{
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("hhhhhhh");
      lcd.setCursor(0,1);
      lcd.print("hhhhhh");
    } break;
    case 3:{
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Tfsaf");
      lcd.setCursor(0,1);
      lcd.print("adsfdsf");
    }
  }
}
