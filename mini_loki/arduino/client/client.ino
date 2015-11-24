/*
 *  This sketch sends data via HTTP GET requests to data.sparkfun.com service.
 *
 *  You need to get streamId and privateKey at data.sparkfun.com and paste them
 *  below. Or just customize this script to talk to other HTTP servers.
 *
 */

#include <ESP8266WiFi.h>

const char* ssid     = "**************";  //  your network SSID (name)
const char* password = "*****************";       // your network password

const char* host = "172.16.17.210";

void setup() {
  Serial.begin(115200);
  delay(10);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

void loop() {
  delay(5000);
  WiFiClient client;
  const int httpPort = 5033;
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
  }
  delay(10);
  while(client.connected()){
    while(client.available()){
      char line = client.read();
      Serial.print(line);
    }
    client.print("Hola Mundo!");
  }
}

