// solve the interference with a resistor
// https://arduino.stackexchange.com/questions/1263/interference-at-digital-input-uno

const int boardNo = 0;
const int buttonPins[] = {2, 5, 7, 8};
const int buttonCount = sizeof(buttonPins)/sizeof(int);
int buttonStates[buttonCount];
int lastButtonStates[buttonCount];

void setup() {
  for (int i=0; i <= buttonCount - 1; i++) {
    pinMode(i, INPUT_PULLUP);
    buttonStates[i] = HIGH;
    lastButtonStates[i] = HIGH;
  }
  Serial.begin(9600);
  Serial.println("Ready");
  Serial.print("i");
  Serial.println(buttonCount);
}

void loop() {
  for (int i=0; i <= buttonCount - 1; i++) {
    
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
      if (buttonStates[i] == LOW) {
        Serial.println(1);
        lastButtonStates[i] = LOW;
      } else {
        Serial.println(0);
        lastButtonStates[i] = HIGH;
      }
      delay(50);
    }
    
  }

}
