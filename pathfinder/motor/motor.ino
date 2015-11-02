
#include <Wire.h>

int speed2Pin = 9;
int direction2Pin = 6;
int speed1Pin = 10;
int direction1Pin = 7;
int speed0Pin = 11;
int direction0Pin = 8;

float speed_0 = 0;
float speed_1 = 0;
float speed_2 = 0;
float camera_position;

String input;
String incoming;

boolean stringComplete = false;
boolean startMessage = false;

void setup() {
  Wire.begin(8);
  Wire.onReceive(receiveEvent); // register event
  pinMode(direction0Pin, OUTPUT);
  pinMode(direction1Pin, OUTPUT);
  pinMode(direction2Pin, OUTPUT);
  set_speed(0, 0);
  set_speed(1, 0);
  set_speed(2, 0);
}

void loop() {
  if (stringComplete) {
    incoming = input;
    parse_string(incoming);
    stringComplete = false;
  }
}

void receiveEvent(int howMany) {
  char inChar;
  while (Wire.available()) {
    inChar = Wire.read();
    if (inChar == ')') {
      startMessage = false;
      stringComplete = true;
      input += ',';
    }
    if (startMessage) input += inChar;
    if (inChar == '(' && !startMessage) startMessage = true;
    if (inChar == '(' && startMessage) input = "";
    delay(3);
    if (stringComplete) break;
  }
}

void parse_string(String inputString) {
  int message_substring = 0;
  String substr = "";
  for (int i = 0 ; i < inputString.length(); i++) {
    if (inputString[i] == ',') {
      message_substring++;
      switch (message_substring) {
        case 1:
          speed_0 = substr.toFloat();
          substr = "";
        case 2:
          speed_1 = substr.toFloat();
          substr = "";
        case 3:
          speed_2 = substr.toFloat();
          substr = "";
        case 4:
          camera_position = substr.toFloat();
          substr = "";
      }
    }
    else substr += (char)inputString[i];
  }
  set_speed(0, speed_0);
  set_speed(1, speed_1);
  set_speed(2, speed_2);
}

void set_speed(int motor, float spd) {
  int dir = LOW;
  if (spd < 0) {
    dir = HIGH;
    spd = 1 + spd;
  }
  switch (motor) {
    case 0:
      digitalWrite(direction0Pin, dir);
      analogWrite(speed0Pin, int(spd * 255.0));
    case 1:
      digitalWrite(direction1Pin, dir);
      analogWrite(speed1Pin, int(spd * 255.0));
    case 2:
      digitalWrite(direction2Pin, dir);
      analogWrite(speed2Pin, int(spd * 255.0));
  }
}
