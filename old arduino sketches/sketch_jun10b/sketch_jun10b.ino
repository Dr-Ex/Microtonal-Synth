const int button1Pin = 2;
const int button2Pin = 3;
int button1State = 0;
int lastButton1State = 0;
int button2State;

void setup() {
  pinMode(button1Pin, INPUT);
  pinMode(button2Pin, INPUT);
  Serial.begin(9600);
  Serial.println("Ready");
}

void loop() {
  button1State = digitalRead(button1Pin);

  if (button1State != lastButton1State) {
    if (button1State == HIGH) {
      Serial.println("Button 1 On");
    } else {
      Serial.println("Button 1 Off");
    }
    delay(50);    
  }
  lastButton1State = button1State;

}
