const int boardNo = 1;
const int buttonCount = 1;
int buttonPins[buttonCount];
//const int buttonCount = sizeof(buttonPins)/sizeof(int);
int buttonStates[buttonCount];
int lastButtonStates[buttonCount];

void setup() {
  
  for (int i=0; i < buttonCount; i++) {
    buttonPins[i] = i+2;
    pinMode(buttonPins[i], INPUT);
    buttonStates[i] = LOW;
    lastButtonStates[i] = LOW;
  }
  Serial.begin(9600);
  Serial.println("Ready");
  Serial.print("i");
  Serial.print(buttonCount);
  Serial.print(" ");
  Serial.println(boardNo);
}

void loop() {
  for (int i=0; i < buttonCount; i++) {
    
//    if (buttonStates[i] == null || lastButtonStates[i] == null) {
//      buttonStates[i] = 0;
//      lastButtonStates[i] = 0;
//    }
    
    buttonStates[i] = digitalRead(buttonPins[i]);

    if (buttonStates[i] != lastButtonStates[i]) {
      Serial.print("n");
      Serial.print(boardNo);
      Serial.print(" ");
      Serial.print(i);
      Serial.print(" ");
      if (buttonStates[i] == HIGH) {
        Serial.println(1);
        lastButtonStates[i] = HIGH;
      } else {
        Serial.println(0);
        lastButtonStates[i] = LOW;
      }
      delay(50);
    }
    
  }

}
