int inSensor1=8;
int inSensor2=9;
int inSensor3=10;

void setup() {
  pinMode (inSensor1, INPUT);
  pinMode (inSensor2, INPUT);
  pinMode (inSensor3, INPUT);

}

void loop() {
  int inSensorDetect1 = digitalRead (inSensor1);
  int inSensorDetect2 = digitalRead (inSensor2);
  int inSensorDetect3 = digitalRead (inSensor3);
  Serial.print("1 :");
  Serial.println(inSensorDetect1);
  Serial.print("2 :");
  Serial.println(inSensorDetect2);
  Serial.print("3 :");
  Serial.println(inSensorDetect3);
  Serial.println();
  delay(2000);

}
