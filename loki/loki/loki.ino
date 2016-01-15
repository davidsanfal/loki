
#include <Servo.h>

/* Arduino pin list */

int speed1Pin = 3;
int direction1Pin = 2;
int speed0Pin = 5;
int direction0Pin = 4;
int speed2Pin = 6;
int direction2Pin = 7;
int laserPinRigth = 8;
int laserPinLeft = 9;
int servoPinRigth = 10;
int servoPinLeft = 11;
int ldrPin = A0;

/* Distance between the center and the wheel's axis  */

float arms_size = 110.74;

/* LDR threshold */

int laser_impact = 210;

/* Other variables */

float speed_0 = 0;
float speed_1 = 0;
float speed_2 = 0;
float speed_X = 0;
float speed_Y = 0;
float speed_W = 0;
int shot = 0;

bool shooting_up = false;
unsigned long previousMillis = 0;
unsigned long previousShotMillis = 0;
unsigned long previousTimeoutMillis = 0;
const long interval = 5000;
const long shot_interval = 150;
const long timeout_interval = 1000;
boolean stringComplete = false;
boolean startMessage = false;
boolean weaponRigth = true;

Servo servoRigth;
Servo servoLeft;

void setup() {
  Serial.begin(19200);
  pinMode(laserPinRigth, OUTPUT);
  pinMode(laserPinLeft, OUTPUT);
  servoRigth.attach(servoPinRigth);
  servoLeft.attach(servoPinLeft);
}

/*
Read a string from the serial port bluetooth with the following structure:
(speed_X;speed_Y;speed_W;shot)

speed_X = -1.00 to 1.00 Float with two decimal
speed_Y = -1.00 to 1.00 Float with two decimal
speed_W = -1.00 to 1.00 Float with two decimal
shot = 0 or 1 Int

This fuction save in inputString a string with the following structure:
speed_X;speed_Y;speed_W;shot;

stringComplete = true when a complete message is received.
*/

String read_string() {
  String inputString = "";
  char inChar;
  while (Serial.available()) {
    inChar = (char)Serial.read();
    if (inChar == ')') {
      startMessage = false;
      stringComplete = true;
      inputString += ';';
    }
    if (startMessage) inputString += inChar;
    if (inChar == '(' && !startMessage) startMessage = true;
    if (inChar == '(' && startMessage) inputString = "";
    delay(1);
    if (stringComplete) break;
  }
  return inputString;
}

/*
Parse the inputString string and update speed_X, speed_Y, speed_W and shot.

At the end, calls combine_movements() to convert the movement in (X, Y, W) to wheels speed.
*/

void parse_string(String inputString) {
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
        case 4:
          shot = substr.toInt();
          substr = "";
      }
    }
    else substr += (char)inputString[i];
  }
  combine_movements();
}

/*
Convert the movement in (X, Y, W) to wheels speed.

http://www.inescporto.pt/~hfpo/papers/Oliveira_CRCS_INTECH.pdf-> equation(2)

At the end, calls set_speed() to set the new wheels speed normalized (-1 to 1). 
*/

void combine_movements() {
  speed_0 = (-speed_X * sin(PI / 3)) + (speed_Y * cos(PI / 3)) + speed_W;
  speed_1 = -speed_Y + speed_W;
  speed_2 = (speed_X * sin(PI / 3)) + (speed_Y * cos(PI / 3)) + speed_W;
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
  set_speed(0, speed_0, norm);
  set_speed(1, speed_1, norm);
  set_speed(2, speed_2, norm);
}

/*
Set wheel speeds using a https://www.pololu.com/product/2990
*/

void set_speed(int motor, float spd, float norm) {
  int dir = 1;
  if (spd < 0) dir = 0;
  spd = map(abs(spd / norm) * 100, 0.0, 100.0, 0, 255);
  switch (motor) {
    case 0:
      digitalWrite(direction0Pin, dir);
      analogWrite(speed0Pin, spd);
    case 1:
      digitalWrite(direction1Pin, dir);
      analogWrite(speed1Pin, spd);
    case 2:
      digitalWrite(direction2Pin, dir);
      analogWrite(speed2Pin, spd);
  }
}

/*
EXPEROIMENTAL (never used)

Function to fire the laser with regular intervals.
*/

void gunshot() {
  unsigned long currentMillis = millis();
  if (shot > 0) {
    if (currentMillis - previousMillis <= interval) {
      shooting_up = true;
    }
    else {
      previousTimeoutMillis = currentMillis;
      shooting_up = false;
    }
    shot = 0;
  }
  else {
    previousMillis = currentMillis;
    shooting_up = false;
  }
  if (shooting_up) {
    if (currentMillis - previousShotMillis <= shot_interval) {
      if (weaponRigth == true) {
        digitalWrite(laserPinRigth, 1);
        digitalWrite(laserPinLeft, 0);
      }
      else {
        digitalWrite(laserPinLeft, 1);
        digitalWrite(laserPinRigth, 0);
      }
    }
    else {
      previousShotMillis = currentMillis;
      weaponRigth = !weaponRigth;
    }
  }
  else {
    previousShotMillis = currentMillis;
    digitalWrite(laserPinRigth, 0);
    digitalWrite(laserPinLeft, 0);
  }
}

/*
EXPEROIMENTAL (never used)

Function to determine if the robot is hit.
*/

boolean shocked() {
  int shocked  = analogRead(ldrPin);
  if (shocked > laser_impact) return true;
  else return false;
}

void stop_robot() {
  analogWrite(speed0Pin, 0);
  analogWrite(speed1Pin, 0);
  analogWrite(speed2Pin, 0);
  digitalWrite(laserPinRigth, 1);
  digitalWrite(laserPinLeft, 1);
}

void loop() {
  // EXPEROIMENTAL (never used): If you use continuously the laser, the robot stop for a while
  /*if (millis() - previousTimeoutMillis <= timeout_interval){
    stop_robot();
    shot = 0;
  }
  else {*/
  //Read and parse the input string
  String incoming;
  if (Serial.available()) incoming = read_string();
  if (stringComplete) {
    parse_string(incoming);
    stringComplete = false;
  }
  // EXPEROIMENTAL (never used)
  //gunshot();
  //shot = 1;
  //shooting_up = false;
  servoRigth.write(85);
  servoLeft.write(85);
  //}
}

