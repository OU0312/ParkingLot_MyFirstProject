extern volatile unsigned long timer0_millis; //타이머변수
unsigned long readTime; //현재타이머시간
int hour, min, sec;
int hour2, min2, sec2;

long dev;

void setup()
{
  Serial.begin(9600);
//  Serial.println(__TIME__);

  String inString = __TIME__;
  int index1 = inString.indexOf(':');
  int index2 = inString.indexOf(':', index1 + 1);
  int index3 = inString.length();

  hour = inString.substring(0, index1).toInt();
  min = inString.substring(index1 + 1, index2).toInt();
  sec = inString.substring(index2 + 1, index3).toInt();

  timer0_millis = ((long)hour * 3600 + min * 60 + sec) * 1000;
}

void loop()
{
  readTime = millis() / 1000;
  sec = readTime % 60;
  min = (readTime / 60) % 60;
  hour = (readTime / (60 * 60)) % 24;

  // 초당 1임 1분이면 60 10분이면 600
  dev = readTime + 600;
  sec2 = dev % 60;
  min2 = (dev / 60) % 60;
  hour2 = (dev / (60 * 60)) % 24;
  
  //Serial.println(__DATE__);

  Serial.print(readTime);
  Serial.print("  /  ");
  Serial.println(dev);
  Serial.print(hour);
  Serial.print(" : ");
  Serial.print(min);
  Serial.print(" : ");
  Serial.println(sec);
  
  Serial.print(hour2);
  Serial.print(" : ");
  Serial.print(min2);
  Serial.print(" : ");
  Serial.println(sec2);
  delay (5000);
}
