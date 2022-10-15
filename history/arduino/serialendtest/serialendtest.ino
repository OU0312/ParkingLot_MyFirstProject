void setup() {
  
}
 
void loop() {
  Serial.begin(9600);
  Serial.println("Hello!!");
  delay(3000);
  Serial.end();
  Serial.println("Bye!!");
}
