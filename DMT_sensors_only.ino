#include <dht.h>

dht DHT;
#define DHT11_PIN 2

int cnt = 0;

void setup() {
  Serial.begin(9600);

  Serial.println("<Arduino is ready>");
}

int get_soil_moisture() {
  int extreme_when_wet = 0;
  int extreme_when_dry = 551;

  int raw_input = analogRead(A0);
  int processed_input = min(max(extreme_when_wet, raw_input), extreme_when_dry);

  int percentage_of_dryness = map(processed_input, extreme_when_wet, extreme_when_dry, 0, 100);
  int percentage_of_wetness = 100 - percentage_of_dryness;

  return percentage_of_wetness;
}

int get_humidity() {
  return DHT.humidity;
}

int get_temperature() {
  return DHT.temperature;
}

void loop() {
  int chk = DHT.read11(DHT11_PIN);

  Serial.println("<"+
                 String(get_soil_moisture())+","+
                 String(get_humidity())+","+
                 String(get_temperature())+","+
                 String(cnt)+
                 ">");
  cnt++;

  delay(16000);        // delay in between reads for stability
}

