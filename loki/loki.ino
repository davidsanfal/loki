/*
 Fading

 This example shows how to fade an LED using the analogWrite() function.

 The circuit:
 * LED attached from digital pin 9 to ground.

 Created 1 Nov 2008
 By David A. Mellis
 modified 30 Aug 2011
 By Tom Igoe

 http://www.arduino.cc/en/Tutorial/Fading

 This example code is in the public domain.

 */


int speed1Pin = 3;
int direction1Pin = 2;
int speed0Pin = 5;
int direction0Pin = 4;
int speed2Pin = 6;
int direction2Pin = 7;

float arms_size = 110.74;

float speed_0 = 0;
float speed_1 = 0;
float speed_2 = 0;
float speed_X = 0;
float speed_Y = 0;
float speed_W = 0;

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete
boolean startMessage = false;

void setup() {
  Serial.begin(19200);
}

void loop() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();

    if (inChar == ')') {
      startMessage = false;
      stringComplete = true;
      inputString += ';';
      Serial.flush();
    }
    if (startMessage) inputString += inChar;
    if (inChar == '(' && !startMessage) startMessage = true;
    if (inChar == '(' && startMessage) inputString = "";
    if (stringComplete) break;
  }
  if (stringComplete) {
    int message_substring = 0;
    String substr = "";
    for (int i = 0 ; i < inputString.length(); i++) {
      if (inputString[i] == ';') {
        message_substring++;
        switch (message_substring) {
          case 1:
            speed_X = substr.toFloat();
            substr = "";
          case 2:
            speed_Y = substr.toFloat();
            substr = "";
          case 3:
            speed_W = substr.toFloat();
            substr = "";
        }
      }
      else substr += (char)inputString[i];
    }
    inputString = "";
    stringComplete = false;
    combine_movements();
  }
}

void combine_movements() {

  speed_0 = (-speed_X / sin(PI / 3)) + (speed_Y / cos(PI / 3)) + (arms_size * speed_W);
  speed_1 = (-speed_Y + arms_size * speed_W);
  speed_2 = (speed_X / sin(PI / 3)) + (speed_Y / cos(PI / 3)) + (arms_size * speed_W);
  float norm = 1.0;
  if (abs(speed_0) > 1 || abs(speed_1) > 1 || abs(speed_2) > 1) {
    if (abs(speed_0) >= abs(speed_1)) {
      norm = abs(speed_0);
      if (abs(speed_2) > abs(speed_0)) norm = abs(speed_2);

    }
    else {
      norm = abs(speed_1);
      if (abs(speed_2) > abs(speed_1)) norm = abs(speed_2);
    }
  }

  speed_0 = map(abs(speed_0/norm), 0, 1.0, 0, 255);
  speed_1 = map(abs(speed_0/norm), 0, 1.0, 0, 255);
  speed_2 = map(abs(speed_0/norm), 0, 1.0, 0, 255);
}

void counterclockwise() {
  digitalWrite(direction0Pin, 1);
  analogWrite(speed0Pin, 150);
  digitalWrite(direction2Pin, 1);
  analogWrite(speed2Pin, 150);
  digitalWrite(direction1Pin, 1);
  analogWrite(speed1Pin, 150);
}
