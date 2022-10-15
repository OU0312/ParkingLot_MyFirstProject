#include<Servo.h>
#include<LiquidCrystal_I2C_Hangul.h>
#include<LiquidCrystal_I2C.h>
#include<Wire.h>

//Mux control point
int s0=8;
int s1=9;
int s2=10;
int s3=11;
int SIG_Pin=0;
int controlPin[] = {s0,s1,s2,s3};
int muxChannel[16][4]={ {0,0,0,0}, // Channel 0
    {1,0,0,0}, // Channel 1
    {0,1,0,0}, // Channel 2
    {1,1,0,0}, // Channel 3
    {0,0,1,0}, // Channel 4
    {1,0,1,0}, // Channel 5
    {0,1,1,0}, // Channel 6
    {1,1,1,0}, // Channel 7
    {0,0,0,1}, // Channel 8
    {1,0,0,1}, // Channel 9
    {0,1,0,1}, // Channel 10
    {1,1,0,1}, // Channel 11
    {0,0,1,1}, // Channel 12
    {1,0,1,1}, // Channel 13
    {0,1,1,1}, // Channel 14
    {1,1,1,1} // Channel 15
}; 


// Servo
Servo servo1;
Servo servo2;
int servo1Pin=5;
int servo2Pin=6;

// LCD
LiquidCrystal_I2C lcd_inside (0x26,16,2); // 안쪽 LCD
LiquidCrystal_I2C lcd_out (0x27,16,2); // 출구 LCD
LiquidCrystal_I2C lcd_in (0x3F,16,2); // 입구 LCD

int lcdstate;
int totalspace[9];
int total;
int leftspace[4];
int left;
int rightspace[4];
int right;

void setup() {
  servo1.attach(servo1Pin);
  servo2.attach(servo2Pin);
  servo1.write(5);
  servo2.write(10);
  
  pinMode(s0,OUTPUT);
  pinMode(s1,OUTPUT);
  pinMode(s2,OUTPUT);
  pinMode(s3,OUTPUT);

  digitalWrite(s0,LOW);
  digitalWrite(s1,LOW);
  digitalWrite(s2,LOW);
  digitalWrite(s3,LOW);

  lcd_inside.init();
  lcd_inside.backlight();
  lcd_inside.clear();
  //lcd_inside.print("lcd_inside");
  
  lcd_out.init();
  lcd_out.backlight();
  lcd_out.clear();
  lcd_out.print("lcd_out");

  lcd_in.init();
  lcd_in.backlight();
  lcd_in.clear();
  lcd_in.print("lcd_in");

  Serial.begin(9600);
}

void loop() {
  totalcheck();
}

void lcdCheck(){
  switch(lcdstate){
    case 1:{ 
      totallcd();
    }break;
    case 9:{ 
    }break;
  }
}

void totallcd(){
//  lcd_inside.clear();
  lcd_inside.setCursor(3,0);
  lcd_inside.print("Total : ");
  
  lcd_inside.print(total);
  lcd_inside.setCursor(0,1);
  lcd_inside.print(left);
  lcd_inside.setCursor(5,1);
  lcd_inside.print("<==");
  lcd_inside.setCursor(8,1);
  lcd_inside.print("==>");
  lcd_inside.setCursor(15,1);
  lcd_inside.print(right);
}




void totalcheck(){
  
//  for(int i=0; i<=9; i++){
//    if(readMux(i)<=100){
//      totalspace[i]=0;
//    }else{
//      totalspace[i]=1;
//    }
//  }
//
//  returntotal();

  
  leftcheck();
  rightcheck();

  total=left+right;
  lcdstate=1;
  lcdCheck();

}

//void returntotal(){
//  total=0;
//  for(int i=0; i<10; i++){
//    total=total+totalspace[i];
//  }
//
//  leftcheck();
//  rightcheck();
//  lcdstate=1;
//  lcdCheck();
//}

void leftcheck(){
  int j=0;
  for(int i=5; i<=9; i++){
    if(readMux(i)<=100){
      leftspace[j]=0;
    }else{
      leftspace[j]=1;
    }
    j++;
    }

  returnleft();
}

void returnleft(){
  left=0;
  for(int i=0; i<5; i++){
    left=left+leftspace[i];
  }
}

void rightcheck(){
  for(int i=0; i<=4; i++){
    if(readMux(i)<=100){
      rightspace[i]=0;
    }else{
      rightspace[i]=1;
    }
  }

  returnright();
}

void returnright(){
  right=0;
  for(int i=0; i<5; i++){
    right=right+rightspace[i];
  }
}
void Muxtest(){
  for(int i=0; i<16; i++){
    Serial.print("Value at Channel (");
    Serial.print(i); Serial.print("): ");
    Serial.println(readMux(i));
    delay(1000);
  }
}

int readMux(int channel){
  for(int i=0; i<4; i++){
    digitalWrite(controlPin[i],muxChannel[channel][i]);
  }
  int val=analogRead(SIG_Pin);
  return val;
}

void servotest(){
  servo1.write(85);
  servo2.write(90);
  delay(1000);
  servo1.write(5);
  servo2.write(10);
  delay(1000);
}
