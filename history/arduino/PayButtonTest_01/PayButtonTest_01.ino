int buttonApin = 12;
 
 
void setup() 
{
  Serial.begin(9600);
  pinMode(buttonApin, INPUT_PULLUP); 
}
 
void loop() 
{
  if (digitalRead(buttonApin) == LOW)
  {
    Serial.println("LOW");
  }
}
