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


int speed3Pin = 3;
int direction3Pin = 2;
int speed1Pin = 5;
int direction1Pin = 4;
int speed2Pin = 6;
int direction2Pin = 7;

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete


void setup(){

  Serial.begin(19200);

  // reserve 200 bytes for the inputString:
  inputString.reserve(200);
}

void loop() {
  serialEvent(); //call the function
  // print the string when a newline arrives:
  if (stringComplete) {
    if(inputString == "r"){
      right();
    }
    if(inputString == "l"){
      left();
    }
    if(inputString == "f"){
      front();
    }
    if(inputString == "b"){
      back();
    }
    if(inputString == "c"){
      clockwise();
    }
    if(inputString == "a"){
      counterclockwise();
    }
    if(inputString == "s"){
      stop_all();
    }
    Serial.println(inputString);
    // clear the string:
    inputString = "";
    stringComplete = false;
  }
}

/*
  SerialEvent occurs whenever a new data comes in the
 hardware serial RX.  This routine is run between each
 time loop() runs, so using delay inside loop can delay
 response.  Multiple bytes of data may be available.
 */
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
    else{
      // add it to the inputString:
      inputString += inChar;
    }
  }
}

void front(){
  digitalWrite(direction1Pin, 0);
  analogWrite(speed1Pin, 255);
  digitalWrite(direction2Pin, 1);
  analogWrite(speed2Pin, 255);
  analogWrite(speed3Pin, 0);
  }

void back(){
  digitalWrite(direction1Pin, 1);
  analogWrite(speed1Pin, 255);
  digitalWrite(direction2Pin, 0);
  analogWrite(speed2Pin, 255);
  analogWrite(speed3Pin, 0);
  }

void stop_all(){
  analogWrite(speed1Pin, 0);
  analogWrite(speed2Pin, 0);
  analogWrite(speed3Pin, 0);
  }
  

void left(){
  digitalWrite(direction1Pin, 1);
  analogWrite(speed1Pin, 125);
  digitalWrite(direction2Pin, 1);
  analogWrite(speed2Pin, 125);
  digitalWrite(direction3Pin, 0);
  analogWrite(speed3Pin, 255);
  }

void right(){
  digitalWrite(direction1Pin, 0);
  analogWrite(speed1Pin, 125);
  digitalWrite(direction2Pin, 0);
  analogWrite(speed2Pin, 125);
  digitalWrite(direction3Pin, 1);
  analogWrite(speed3Pin, 255);
  }

void clockwise(){
  digitalWrite(direction1Pin, 0);
  analogWrite(speed1Pin, 255);
  digitalWrite(direction2Pin, 0);
  analogWrite(speed2Pin, 255);
  digitalWrite(direction3Pin, 0);
  analogWrite(speed3Pin, 255);
  }

void counterclockwise(){
  digitalWrite(direction1Pin, 1);
  analogWrite(speed1Pin, 255);
  digitalWrite(direction2Pin, 1);
  analogWrite(speed2Pin, 255);
  digitalWrite(direction3Pin, 1);
  analogWrite(speed3Pin, 255);
  }
