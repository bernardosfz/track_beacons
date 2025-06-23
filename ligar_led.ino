int ledPin = 3;

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char receivedChar = Serial.read();
    if (receivedChar == '1') {
      digitalWrite(ledPin, HIGH);
      delay(5000);
      digitalWrite(ledPin, LOW);
    }
  }
}
