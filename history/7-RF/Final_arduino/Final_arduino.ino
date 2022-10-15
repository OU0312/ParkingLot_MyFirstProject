#include<Servo.h>
#include<SoftwareSerial.h>
#include<LiquidCrystal_I2C.h>
#include<Wire.h>
#include "Keyboard.h"

//Mux control point
int s0 = 8;
int s1 = 9;
int s2 = 10;
int s3 = 11;
int SIG_Pin = 0;
int controlPin[] = {s0, s1, s2, s3};
int muxChannel[16][4] = { {0, 0, 0, 0}, // Channel 0
  {1, 0, 0, 0}, // Channel 1
  {0, 1, 0, 0}, // Channel 2
  {1, 1, 0, 0}, // Channel 3
  {0, 0, 1, 0}, // Channel 4
  {1, 0, 1, 0}, // Channel 5
  {0, 1, 1, 0}, // Channel 6
  {1, 1, 1, 0}, // Channel 7
  {0, 0, 0, 1}, // Channel 8
  {1, 0, 0, 1}, // Channel 9
  {0, 1, 0, 1}, // Channel 10
  {1, 1, 0, 1}, // Channel 11
  {0, 0, 1, 1}, // Channel 12
  {1, 0, 1, 1}, // Channel 13
  {0, 1, 1, 1}, // Channel 14
  {1, 1, 1, 1} // Channel 15
};

// Timer
extern volatile unsigned long timer0_millis; //타이머변수
unsigned long readTime; //현재타이머시간
int hour, min, sec;


// Servo
Servo servo_in;
Servo servo_out;
int servo1Pin = 5;
int servo2Pin = 6;


// RYG
int rPin = A5;
int yPin = A4;
int gPin = A3;

// LCD
LiquidCrystal_I2C lcd_inside (0x26, 16, 2); // 안쪽 LCD
LiquidCrystal_I2C lcd_out (0x27, 16, 2); // 출구 LCD
LiquidCrystal_I2C lcd_in (0x23, 16, 2); // 입구 LCD

int total;
int totalten = LOW;
int leftspace[4];
int left;
int rightspace[4];
int right;

// gatecontorl
int ingatestate = HIGH;
int outgatestate = HIGH;
int inwelcomeState = LOW;
int outwelcomeState = LOW;

// LCD with python
char cmd;
int cmdvalue;
int cnt = 0;
int allnum[7];
int timenum[4];
char cmd_h;
int inLcdState = 0;
int inseven = LOW;
int inerrorseven = LOW;
int innormal = LOW;

int outLcdState = 0;
int outseven = LOW;
int outerrorseven = LOW;
int outnormal = LOW;

// pay
int paywon;
int paybutton = 12;
long dev;
long timediff;
long ga_in;
long na_in;
long da_in;
long ra_in;
long ma_in;
long ba_in;
long sa_in;
long ah_in;
long oo_in;
long ja_in;
long ha_in;

// LCD Hangul

byte kk[] = {
  0x00,
  0x08,
  0x08,
  0x0E,
  0x08,
  0x08,
  0x08,
  0x00
};


byte gg[] = {
  0x00,
  0x00,
  0x0E,
  0x02,
  0x02,
  0x02,
  0x00,
  0x00
};

byte nn[] = {
  0x00,
  0x00,
  0x08,
  0x08,
  0x08,
  0x0E,
  0x00,
  0x00
};

byte dd[] = {
  0x00,
  0x00,
  0x0E,
  0x08,
  0x08,
  0x08,
  0x0E,
  0x00
};

byte rr[] = {
  0x00,
  0x00,
  0x0E,
  0x02,
  0x0E,
  0x08,
  0x0E,
  0x00
};

byte mm[] = {
  0x00,
  0x00,
  0x0E,
  0x0A,
  0x0A,
  0x0E,
  0x00,
  0x00
};

byte bb[] = {
  0x00,
  0x00,
  0x0A,
  0x0A,
  0x0E,
  0x0A,
  0x0E,
  0x00
};

byte ss[] = {
  0x00,
  0x00,
  0x04,
  0x0A,
  0x11,
  0x00,
  0x00,
  0x00
};

byte hh[] = {
  B00000,
  B00100,
  B11111,
  B00100,
  B01010,
  B01010,
  B00100,
  B00000
};

byte aa[] = {
  0x00,
  0x04,
  0x0A,
  0x0A,
  0x0A,
  0x0A,
  0x04,
  0x00
};

byte jj[] = {
  0x00,
  0x00,
  0x0E,
  0x02,
  0x04,
  0x0A,
  0x00,
  0x00
};

//byte oo[] = {
//  0x00,
//  0x02,
//  0x02,
//  0x0E,
//  0x02,
//  0x02,
//  0x02,
//  0x00
//};

byte oo[] = {
  0x01,
  0x01,
  0x01,
  0x1F,
  0x01,
  0x01,
  0x01,
  0x01
};

void setup() {
  // Timer
  Serial.begin (9600);
  
  String inString = __TIME__;
  int index1 = inString.indexOf(':');
  int index2 = inString.indexOf(':', index1 + 1);
  int index3 = inString.length();

  hour = inString.substring(0, index1).toInt();
  min = inString.substring(index1 + 1, index2).toInt();
  sec = inString.substring(index2 + 1, index3).toInt();

  timer0_millis = ((long)hour * 3600 + min * 60 + sec) * 1000;

  // Servo
  servo_in.attach(servo1Pin);
  servo_out.attach(servo2Pin);
  servo_in.write(65);
  servo_out.write(70);

  // MUX
  pinMode(s0, OUTPUT);
  pinMode(s1, OUTPUT);
  pinMode(s2, OUTPUT);
  pinMode(s3, OUTPUT);

  digitalWrite(s0, LOW);
  digitalWrite(s1, LOW);
  digitalWrite(s2, LOW);
  digitalWrite(s3, LOW);

  // Pay
  pinMode(paybutton, INPUT_PULLUP);

  // LCD
  lcd_inside.init();
  lcd_inside.backlight();
  lcd_inside.clear();

  lcd_out.init();
  lcd_out.backlight();
  lcd_out.clear();
  outnormalprint();


  lcd_in.init();
  lcd_in.backlight();
  lcd_in.clear();
  innormalprint();


  lcd_in.createChar(0, kk);
  lcd_out.createChar(0, kk);
}

void loop() {
  if (inwelcomeState == LOW) {
    intimetest();
  }
  if (outwelcomeState == LOW) {
    outtimetest();
  }
  totalcheck();
  inSensorCheck();
  outSensorCheck();
}


// System

void intimetest() {
  readTime = millis() / 1000;
  sec = readTime % 60;
  min = (readTime / 60) % 60;
  hour = (readTime / (60 * 60)) % 24;

  //Serial.println(__DATE__);
  static unsigned long currTime = 0;
  static unsigned long prevTime = 0;

  currTime = millis();
  if (currTime - prevTime >= 1000)
  {
    innormalprint();
  }

  //delay (1000);
}

void outtimetest() {
  readTime = millis() / 1000;
  sec = readTime % 60;
  min = (readTime / 60) % 60;
  hour = (readTime / (60 * 60)) % 24;

  //Serial.println(__DATE__);
  static unsigned long currTime = 0;
  static unsigned long prevTime = 0;
  currTime = millis();
  if (currTime - prevTime >= 1000)
  {
    outnormalprint();
  }
  //delay (1000);
}
int readMux(int channel) {
  for (int i = 0; i < 4; i++) {
    digitalWrite(controlPin[i], muxChannel[channel][i]);
  }
  int val = analogRead(SIG_Pin);
  return val;
}

// Inside
void totallcd() {
  static unsigned long currTime = 0;
  static unsigned long prevTime = 0;

  currTime = millis();
  if (currTime - prevTime >= 1000)
  {
    prevTime = currTime;
    lcd_inside.setCursor(3, 0);
    lcd_inside.print("Total : ");
    lcd_inside.print(total);
    lcd_inside.setCursor(0, 1);
    lcd_inside.print(left);
    lcd_inside.setCursor(5, 1);
    lcd_inside.print("<==");
    lcd_inside.setCursor(8, 1);
    lcd_inside.print("==>");
    lcd_inside.setCursor(15, 1);
    lcd_inside.print(right);
  }


}

void totalcheck() {

  leftcheck();
  rightcheck();

  total = left + right;
  if (total == 10) {
    totalten = HIGH;
  }
  if (totalten == HIGH && total != 10) {
    lcd_inside.clear();
    totalten = LOW;
  }
  totallcd();


  // ryg
  if (total == 0) {
    analogWrite(rPin, 1024);
    analogWrite(yPin, 0);
    analogWrite(gPin, 0);
  } else if (total == 1) {
    analogWrite(rPin, 0);
    analogWrite(yPin, 1024);
    analogWrite(gPin, 0);
  } else {
    analogWrite(rPin, 0);
    analogWrite(yPin, 0);
    analogWrite(gPin, 1024);
  }

}

void leftcheck() {
  int j = 0;
  for (int i = 5; i <= 9; i++) {
    if (readMux(i) <= 100) {
      leftspace[j] = 0;
    } else {
      leftspace[j] = 1;
    }
    j++;
  }

  returnleft();
}

void returnleft() {
  left = 0;
  for (int i = 0; i < 5; i++) {
    left = left + leftspace[i];
  }
}

void rightcheck() {
  for (int i = 0; i <= 4; i++) {
    if (readMux(i) <= 100) {
      rightspace[i] = 0;
    } else {
      rightspace[i] = 1;
    }
  }

  returnright();
}

void returnright() {
  right = 0;
  for (int i = 0; i < 5; i++) {
    right = right + rightspace[i];
  }
}


// In

void inpythonCheck() {
  if (Serial.available()) {
    cmd = Serial.read();
    if (cmd == 'e') {
      inLcdState = 9; // 9 error
    }
    else if (cmd == 'g' || cmd == 'n' || cmd == 'd' || cmd == 'r' || cmd == 'm' || cmd == 'b' || cmd == 's' || cmd == 'a' || cmd == 'o' || cmd == 'j' || cmd == 'h' )
    {
      cmd_h = cmd;
      inLcdState = 1;
      //delay(100);
    }
  }
}

void inSensorCheck() {
  // inSD1 10
  // insD2 11
  // insD3 12


  if (readMux(10) <= 100 && readMux(12) >= 100 && inwelcomeState == LOW)
  {
    //Serial.begin (9600);
    //Serial.println("1번센서 작동");
    inLcdState = 2;
    inLcdCheck();
    inwelcomeState = HIGH;
    //delay(500);
  } else if (readMux(11) <= 100 && inwelcomeState == HIGH) {
    //Serial.println("2번센서 작동");
    //delay(500);
    if (inseven != HIGH) {
      Keyboard.write('i');
      Keyboard.releaseAll();
      delay(500);
      inpythonCheck();

    } else if (inerrorseven == HIGH) {
      Keyboard.write('i');
      Keyboard.releaseAll();
      delay(500);
      inpythonCheck();
    }
    inLcdCheck();
    delay(500);
  }
  else if (readMux(12) <= 100)
  {
    Serial.println("3번센서 작동");
    //Keyboard.write('p'); 전시할때 켜야함
    ingatestate = LOW;
    delay(500);
  }
  else if (ingatestate == LOW && readMux(10) >= 100 && readMux(12) >= 100 && inwelcomeState == HIGH)
  {
    servo_in.write(65);
    //Serial.println('1');
    //delay(500);
    ingatestate = HIGH;
    inwelcomeState = LOW;
    inseven = LOW;
    inLcdState = 3;
    inLcdCheck();
    /*cmd = '0';
    cmd_h = '0';*/
    delay(500);
  }
}

void inLcdCheck() {
  switch (inLcdState) {
    case 1: { // 번호판 출력
        inseven = HIGH;
        inerrorseven = LOW;
        inLcdPrint();
        servo_in.write(5);
      } break;
    case 2:
      {
        incomeslowprint();
      } break;
    case 3:
      {
        innormalprint();
      } break;
    case 9: { // 에러
        inerrorseven = HIGH;
        inerrorlcdprint();
      } break;
  }
}

void inLcdPrint() {
  lcd_in.clear();
  if (cmd_h == 'g') {
    lcd_in.setCursor(0, 0);
    lcd_in.print("123");
    //lcd_in.printHangul(L"가",3,1);
    lcd_in.createChar(1, gg);
    lcd_in.setCursor(3, 0);
    lcd_in.write(1);
    lcd_in.setCursor(4, 0);
    lcd_in.write(0);
    lcd_in.setCursor(5, 0);
    lcd_in.print("4567");
    ga_in = millis() / 1000;
  } else if (cmd_h == 'n') {
    lcd_in.print(261);
    lcd_in.setCursor(3, 0);
    //lcd_in.printHangul(L"나",3,1);
    lcd_in.createChar(1, nn);
    lcd_in.setCursor(3, 0);
    lcd_in.write(1);
    lcd_in.setCursor(4, 0);
    lcd_in.write(0);
    lcd_in.setCursor(5, 0);
    lcd_in.print(6752);
    na_in = millis() / 1000;
  } else if (cmd_h == 'd') {
    lcd_in.print(321);
    lcd_in.setCursor(3, 0);
    //lcd_in.printHangul(L"다",3,1);
    lcd_in.createChar(1, dd);
    lcd_in.setCursor(3, 0);
    lcd_in.write(1);
    lcd_in.setCursor(4, 0);
    lcd_in.write(0);
    lcd_in.setCursor(5, 0);
    lcd_in.print(9981);
    da_in = millis() / 1000;
  } else if (cmd_h == 'r') {
    lcd_in.print(450);
    lcd_in.setCursor(3, 0);
    //lcd_in.printHangul(L"라",3,1);
    lcd_in.createChar(1, rr);
    lcd_in.setCursor(3, 0);
    lcd_in.write(1);
    lcd_in.setCursor(4, 0);
    lcd_in.write(0);
    lcd_in.setCursor(5, 0);
    lcd_in.print(2512);
    ra_in = millis() / 1000;
  } else if (cmd_h == 'm') {
    lcd_in.print(565);
    lcd_in.setCursor(3, 0);
    //lcd_in.printHangul(L"마",3,1);
    lcd_in.createChar(1, mm);
    lcd_in.setCursor(3, 0);
    lcd_in.write(1);
    lcd_in.setCursor(4, 0);
    lcd_in.write(0);
    lcd_in.setCursor(5, 0);
    lcd_in.print(2547);
    ma_in = millis() / 1000;
  } else if (cmd_h == 'b') {
    lcd_in.print(951);
    lcd_in.setCursor(3, 0);
    //lcd_in.printHangul(L"바",3,1);
    lcd_in.createChar(1, bb);
    lcd_in.setCursor(3, 0);
    lcd_in.write(1);
    lcd_in.setCursor(4, 0);
    lcd_in.write(0);
    lcd_in.setCursor(5, 0);
    lcd_in.print(5452);
    ba_in = millis() / 1000;
  } else if (cmd_h == 's') {
    lcd_in.print(777);
    lcd_in.setCursor(3, 0);
    //lcd_in.printHangul(L"사",3,1);
    lcd_in.createChar(1, ss);
    lcd_in.setCursor(3, 0);
    lcd_in.write(1);
    lcd_in.setCursor(4, 0);
    lcd_in.write(0);
    lcd_in.setCursor(5, 0);
    lcd_in.print(7777);
    sa_in = millis() / 1000;
  } else if (cmd_h == 'a') {
    lcd_in.print(678);
    lcd_in.setCursor(3, 0);
    //lcd_in.printHangul(L"아",3,1);
    lcd_in.createChar(1, aa);
    lcd_in.setCursor(3, 0);
    lcd_in.write(1);
    lcd_in.setCursor(4, 0);
    lcd_in.write(0);
    lcd_in.setCursor(5, 0);
    lcd_in.print(1229);
    ah_in = millis() / 1000;
  } else if (cmd_h == 'o') {
    lcd_in.print(570);
    lcd_in.setCursor(3, 0);
    //lcd_in.printHangul(L"어",3,1);
    lcd_in.createChar(1, aa);
    lcd_in.createChar(2, oo);
    lcd_in.setCursor(3, 0);
    lcd_in.write(1);
    lcd_in.setCursor(4, 0);
    lcd_in.write(2);
    lcd_in.setCursor(5, 0);
    lcd_in.print(5971);
    oo_in = millis() / 1000;
  } else if (cmd_h == 'j') {
    lcd_in.print(789);
    lcd_in.setCursor(3, 0);
    //lcd_in.printHangul(L"자",3,1);
    lcd_in.createChar(1, jj);
    lcd_in.setCursor(3, 0);
    lcd_in.write(1);
    lcd_in.setCursor(4, 0);
    lcd_in.write(0);
    lcd_in.setCursor(5, 0);
    lcd_in.print(4123);
    ja_in = millis() / 1000;
  }
  else if (cmd_h == 'h') {
    lcd_in.print(234);
    lcd_in.setCursor(3, 0);
    //lcd_in.printHangul(L"하",3,1);
    lcd_in.createChar(1, hh);
    lcd_in.setCursor(3, 0);
    lcd_in.write(1);
    lcd_in.setCursor(4, 0);
    lcd_in.write(0);
    lcd_in.setCursor(5, 0);
    lcd_in.print(5678);
    ha_in = millis() / 1000;
  }
  lcd_in.setCursor(0, 1);
  lcd_in.print("Welcome!");
}

void inerrorlcdprint() {
  static unsigned long currTime = 0;
  static unsigned long prevTime = 0;

  currTime = millis();
  if (currTime - prevTime >= 1000)
  {
    lcd_in.clear();
    lcd_in.print("Wait a moment");
  }

}

void incomeslowprint() {
  static unsigned long currTime = 0;
  static unsigned long prevTime = 0;

  currTime = millis();
  if (currTime - prevTime >= 1000)
  {
    lcd_in.clear();
    lcd_in.print("COME SLOW");
  }

}

void innormalprint() {
  static unsigned long currTime = 0;
  static unsigned long prevTime = 0;

  currTime = millis();
  if (currTime - prevTime >= 1000)
  {
    prevTime = currTime;
    lcd_in.clear();
    lcd_in.setCursor(0, 0);
    lcd_in.print("Time : ");
    lcd_in.print(hour);
    lcd_in.print(":");
    lcd_in.print(min);
    lcd_in.setCursor(0, 1);
    lcd_in.print("Left : ");
    lcd_in.setCursor(8, 1);
    lcd_in.print(total);
  }
}

// Out

void outpythonCheck() {
  if (Serial.available()) {
    cmd = Serial.read();
    if (cmd == 'e') {
      outLcdState = 9; // 9 error
    }
    else if (cmd == 'g' || cmd == 'n' || cmd == 'd' || cmd == 'r' || cmd == 'm' || cmd == 'b' || cmd == 's' || cmd == 'a' || cmd == 'o' || cmd == 'j' || cmd == 'h' )
    {
      cmd_h = cmd;
      outLcdState = 1;
      //delay(100);
    }
  }
}

void outSensorCheck() {
  // inSD1 10
  // insD2 11
  // insD3 12

  if (readMux(13) <= 100 && readMux(15) >= 100 && outwelcomeState == LOW)
  {
    //Serial.begin (9600);
    //Serial.println("1번센서 작동");
    outLcdState = 2;
    outLcdCheck();
    outwelcomeState = HIGH;
    //delay(500);
  } else if (readMux(14) <= 100 && outwelcomeState == HIGH) {
    //Serial.println("2번센서 작동");
    //delay(500);
    if (outseven != HIGH) {
      Keyboard.write('o');
      Keyboard.releaseAll();
      delay(500);
      outpythonCheck();
    } else if (outerrorseven == HIGH) {
      Keyboard.write('i');
      Keyboard.releaseAll();
      delay(500);
      outpythonCheck();
    }
    outLcdCheck();
    delay(500);
  }
  else if (readMux(15) <= 100)
  {
    Serial.println("3번센서 작동");
    //Keyboard.write('p'); 전시할때 켜야함
    outgatestate = LOW;
    //delay(1000);
  }
  else if (outgatestate == LOW && readMux(13) >= 100 && readMux(15) >= 100 && outwelcomeState == HIGH)
  {
    servo_out.write(70);
    //delay(1000);
    outgatestate = HIGH;
    outwelcomeState = LOW;
    outseven = LOW;
    outLcdState = 3;
    outLcdCheck();
    cmd = '0';
    cmd_h = '0';
    delay(500);
  }
}

void outLcdCheck() {
  switch (outLcdState) {
    case 1: { // 번호판 출력
        outseven = HIGH;
        outerrorseven = LOW;
        outLcdPrint();
        if (digitalRead(paybutton) == LOW)
        {
          outLcdState = 4;
          outLcdCheck();
        }
      } break;
    case 2:
      {
        outcomeslowprint();
      } break;
    case 3:
      {
        outnormalprint();
      } break;
    case 4:
      {
        outpayprint();
        servo_out.write(5);
      } break;
    case 9: { // 에러
        outerrorseven = HIGH;
        outerrorlcdprint();
      } break;
  }
}

void outLcdPrint() {
  lcd_out.clear();
  if (cmd_h == 'g') {
    lcd_out.setCursor(0, 0);
    lcd_out.print("123");
    //lcd_out.printHangul(L"가",3,1);
    lcd_out.createChar(1, gg);
    lcd_out.setCursor(3, 0);
    lcd_out.write(1);
    lcd_out.setCursor(4, 0);
    lcd_out.write(0);
    lcd_out.setCursor(5, 0);
    lcd_out.print("4567");

    //pay
    dev = millis() / 1000;
    timediff = dev - ga_in;
    paycalc();
  } else if (cmd_h == 'n') {
    lcd_out.print(261);
    lcd_out.setCursor(3, 0);
    //lcd_out.printHangul(L"나",3,1);
    lcd_out.createChar(1, nn);
    lcd_out.setCursor(3, 0);
    lcd_out.write(1);
    lcd_out.setCursor(4, 0);
    lcd_out.write(0);
    lcd_out.setCursor(5, 0);
    lcd_out.print(6752);

    //pay
    dev = millis() / 1000;
    timediff = dev - na_in;
    paycalc();
  } else if (cmd_h == 'd') {
    lcd_out.print(321);
    lcd_out.setCursor(3, 0);
    //lcd_out.printHangul(L"다",3,1);
    lcd_out.createChar(1, dd);
    lcd_out.setCursor(3, 0);
    lcd_out.write(1);
    lcd_out.setCursor(4, 0);
    lcd_out.write(0);
    lcd_out.setCursor(5, 0);
    lcd_out.print(9981);

    //pay
    dev = millis() / 1000;
    timediff = dev - da_in;
    paycalc();
  } else if (cmd_h == 'r') {
    lcd_out.print(450);
    lcd_out.setCursor(3, 0);
    //lcd_in.printHangul(L"라",3,1);
    lcd_out.createChar(1, rr);
    lcd_out.setCursor(3, 0);
    lcd_out.write(1);
    lcd_out.setCursor(4, 0);
    lcd_out.write(0);
    lcd_out.setCursor(5, 0);
    lcd_out.print(2512);

    //pay
    dev = millis() / 1000;
    timediff = dev - ra_in;
    paycalc();
  } else if (cmd_h == 'm') {
    lcd_out.print(565);
    lcd_out.setCursor(3, 0);
    //lcd_out.printHangul(L"마",3,1);
    lcd_out.createChar(1, mm);
    lcd_out.setCursor(3, 0);
    lcd_out.write(1);
    lcd_out.setCursor(4, 0);
    lcd_out.write(0);
    lcd_out.setCursor(5, 0);
    lcd_out.print(2547);

    //pay
    dev = millis() / 1000;
    timediff = dev - ma_in;
    paycalc();
  } else if (cmd_h == 'b') {
    lcd_out.print(951);
    lcd_out.setCursor(3, 0);
    //lcd_out.printHangul(L"바",3,1);
    lcd_out.createChar(1, bb);
    lcd_out.setCursor(3, 0);
    lcd_out.write(1);
    lcd_out.setCursor(4, 0);
    lcd_out.write(0);
    lcd_out.setCursor(5, 0);
    lcd_out.print(5452);

    //pay
    dev = millis() / 1000;
    timediff = dev - ba_in;
    paycalc();
  } else if (cmd_h == 's') {
    lcd_out.print(777);
    lcd_out.setCursor(3, 0);
    //lcd_out.printHangul(L"사",3,1);
    lcd_out.createChar(1, ss);
    lcd_out.setCursor(3, 0);
    lcd_out.write(1);
    lcd_out.setCursor(4, 0);
    lcd_out.write(0);
    lcd_out.setCursor(5, 0);
    lcd_out.print(7777);

    //pay
    dev = millis() / 1000;
    timediff = dev - sa_in;
    paycalc();
  } else if (cmd_h == 'a') {
    lcd_out.print(678);
    lcd_out.setCursor(3, 0);
    //lcd_out.printHangul(L"아",3,1);
    lcd_out.createChar(1, aa);
    lcd_out.setCursor(3, 0);
    lcd_out.write(1);
    lcd_out.setCursor(4, 0);
    lcd_out.write(0);
    lcd_out.setCursor(5, 0);
    lcd_out.print(1229);

    //pay
    dev = millis() / 1000;
    timediff = dev - ah_in;
    paycalc();
  } else if (cmd_h == 'o') {
    lcd_out.print(570);
    lcd_out.setCursor(3, 0);
    //lcd_out.printHangul(L"어",3,1);
    lcd_out.createChar(1, aa);
    lcd_out.setCursor(3, 0);
    lcd_out.write(1);
    lcd_out.setCursor(4, 0);
    lcd_out.createChar(2, oo);
    lcd_out.write(2);
    lcd_out.setCursor(5, 0);
    lcd_out.print(5971);

    //pay
    dev = millis() / 1000;
    timediff = dev - oo_in;
    paycalc();
  } else if (cmd_h == 'j') {
    lcd_out.print(789);
    lcd_out.setCursor(3, 0);
    //lcd_out.printHangul(L"자",3,1);
    lcd_out.createChar(1, jj);
    lcd_out.setCursor(3, 0);
    lcd_out.write(1);
    lcd_out.setCursor(4, 0);
    lcd_out.write(0);
    lcd_out.setCursor(5, 0);
    lcd_out.print(4123);

    //pay
    dev = millis() / 1000;
    timediff = dev - ja_in;
    paycalc();
  }
  else if (cmd_h == 'h') {
    lcd_out.print(234);
    lcd_out.setCursor(3, 0);
    //lcd_out.printHangul(L"하",3,1);
    lcd_out.createChar(1, hh);
    lcd_out.setCursor(3, 0);
    lcd_out.write(1);
    lcd_out.setCursor(4, 0);
    lcd_out.write(0);
    lcd_out.setCursor(5, 0);
    lcd_out.print(5678);

    //pay
    dev = millis() / 1000;
    timediff = dev - ha_in;
    paycalc();
  }
  lcd_out.setCursor(0, 1);
  lcd_out.print("price : ");
  lcd_out.print(paywon);

  if (digitalRead(paybutton) == LOW)
  {
    outLcdState = 4;
    outLcdCheck();
  }
}

void outerrorlcdprint() {
  static unsigned long currTime = 0;
  static unsigned long prevTime = 0;

  currTime = millis();
  if (currTime - prevTime >= 1000)
  {
    lcd_out.clear();
    lcd_out.print("Wait a moment");
  }

}

void outcomeslowprint() {
  static unsigned long currTime = 0;
  static unsigned long prevTime = 0;

  currTime = millis();
  if (currTime - prevTime >= 1000)
  {
    lcd_out.clear();
    lcd_out.print("COME SLOW");
  }

}

void outnormalprint() {
  static unsigned long currTime = 0;
  static unsigned long prevTime = 0;

  currTime = millis();
  if (currTime - prevTime >= 1000)
  {
    prevTime = currTime;
    lcd_out.clear();
    lcd_out.setCursor(0, 0);
    lcd_out.print("Time : ");
    lcd_out.print(hour);
    lcd_out.print(":");
    lcd_out.print(min);
  }

}

void outpayprint() {
  lcd_out.clear();
  lcd_out.setCursor(0, 0);
  lcd_out.print("Payment has");
  lcd_out.setCursor(0, 1);
  lcd_out.print("been completed");
}

void paycalc() {

  if (timediff <= 60) {
    paywon = 1000;
  } else if (timediff <= 120) {
    paywon = 2000;
  } else if (timediff <= 180) {
    paywon = 3000;
  } else if (timediff <= 240) {
    paywon = 4000;
  } else if (timediff <= 300) {
    paywon = 5000;
  } else if (timediff <= 360) {
    paywon = 6000;
  } else if (timediff <= 420) {
    paywon = 7000;
  } else if (timediff <= 480) {
    paywon = 8000;
  } else if (timediff <= 540) {
    paywon = 9000;
  } else if (timediff >= 600) {
    paywon = 9999;
  }

}
//other

void servotest() {
  servo_in.write(65);
  servo_out.write(70);
  delay(1000);
  servo_in.write(5);
  servo_out.write(10);
  delay(1000);
}
