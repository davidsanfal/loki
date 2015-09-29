int speed1Pin = 3;
int direction1Pin = 2;
int speed0Pin = 5;
int direction0Pin = 4;
int speed2Pin = 6;
int direction2Pin = 7;
int laserPin = 8;

float arms_size = 110.74;

float speed_0 = 0;
float speed_1 = 0;
float speed_2 = 0;
float speed_X = 0;
float speed_Y = 0;
float speed_W = 0;
int shot = 0;

bool shooting_up = false;
unsigned long previousMillis = 0;
const long interval = 1000;
const long shot_interval = 500;
boolean stringComplete = false;
boolean startMessage = false;

void setup() {
  Serial.begin(19200);
  pinMode(laserPin, OUTPUT);
}

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

void combine_movements() {
  speed_0 = (-speed_X / sin(PI / 3)) + (-speed_Y * cos(PI / 3)) + speed_W;
  speed_1 = speed_Y + speed_W;
  speed_2 = (speed_X / sin(PI / 3)) + (-speed_Y * cos(PI / 3)) + speed_W;
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

void set_speed(int motor, float spd, float norm) {
  int dir = 1;
  if (spd < 0) dir = 0;
  spd = map(abs(spd / norm)*100, 0.0, 100.0, 0, 255);
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

void gunshot() {
  unsigned long currentMillis = millis();
  if (shot > 0) {
    if (currentMillis - previousMillis >= interval) {
      previousMillis = currentMillis;
      shooting_up = true;
    }
    shot = 0;
  }
  if (shooting_up) {
    if (currentMillis - previousMillis <= shot_interval) {
      digitalWrite(laserPin, 1);
    }
    else {
      shooting_up = false;
      digitalWrite(laserPin, 0);
    }
  }
}

void loop() {
  String incoming;
  if (Serial.available()) incoming = read_string();
  if (stringComplete) {
    parse_string(incoming);
    stringComplete = false;
  }
  gunshot();
}

