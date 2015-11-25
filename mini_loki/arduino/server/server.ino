#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>
#include <WiFiClient.h>

const char* ssid = "***************";
const char* password = "***************";
String input;
boolean stringComplete = false;
float speed_0 = 0;
float speed_1 = 0;
float speed_2 = 0;
float speed_X = 0;
float speed_Y = 0;
float speed_W = 0;

WiFiServer server(80);

void setup(void)
{
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  if (!MDNS.begin("loki")) {
    Serial.println("Error setting up MDNS responder!");
    while (1) {
      delay(1000);
    }
  }
  Serial.println("mDNS responder started");
  server.begin();
  Serial.println("TCP server started");
  MDNS.addService("http", "tcp", 80);
}

void loop(void)
{
  WiFiClient client = server.available();
  if (!client) {
    return;
  }
  Serial.print("Client connected");
  while (client.connected()) {
    while (client.available()) {
      input = client.readStringUntil('\n');
      stringComplete = true;
    }
    if(stringComplete){
    parse_string(input);
    stringComplete = false;
    }
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
  speed_0 = (-speed_X / sin(PI / 3)) + (-speed_Y * cos(PI / 3)) - speed_W;
  speed_1 = speed_Y - speed_W;
  speed_2 = (speed_X / sin(PI / 3)) + (-speed_Y * cos(PI / 3)) - speed_W;
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
  Serial.print(speed_0);
  Serial.print("    ");
  Serial.print(speed_1);
  Serial.print("    ");
  Serial.println(speed_2);
  /*set_speed(0, speed_0);
  set_speed(1, speed_1);
  set_speed(2, speed_2);*/
}

/*void set_speed(int motor, float spd) {
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
}*/

