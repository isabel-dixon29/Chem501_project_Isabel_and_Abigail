#include <ArduinoMqttClient.h>
#include <WiFiNINA.h>
#include <Arduino_BHY2Host.h>
Sensor temp(SENSOR_ID_TEMP);
Sensor humidity(SENSOR_ID_HUM);
Sensor gas(SENSOR_ID_GAS);

char ssid[] = "WiFiName";
char pass[] = "Password";

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

const char broker[] = "fill_name";
int        port     = "fill_name_as_int";
const char topic1[] = "aitime";
const char topic2[] = "aitemperature";
const char topic3[] = "aihumidity";
const char topic4[] = "aigas";

const long interval = 5000;
unsigned long previousMillis = 0;

int count = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  BHY2Host.begin();
  temp.begin();
  humidity.begin();
  gas.begin();

  Serial.print("Attempting to connect to WPA SSID: ");
  Serial.println(ssid);
  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    // failed, retry
    Serial.print(".");
    delay(5000);
  }

  Serial.println("You're connected to the network");
  Serial.println();

  Serial.print("Attempting to connect to the MQTT broker: ");
  Serial.println(broker);

  if (!mqttClient.connect(broker, port)) {
    Serial.print("MQTT connection failed! Error code = ");
    Serial.println(mqttClient.connectError());

    while (1);
  }

  Serial.println("You're connected to the MQTT broker!");
  Serial.println();
}

void loop() {
  // put your main code here, to run repeatedly:
  mqttClient.poll();

  unsigned long startTime = millis();

  float dataT = 0;
  unsigned long currentMillis = millis();

  BHY2Host.update();
  dataT = millis() - startTime;
  float dataTemp = temp.value();
  float dataH = humidity.value();
  float dataG = gas.value();

  if (currentMillis - previousMillis >= interval) {
      // save the last time a message was sent
    previousMillis = currentMillis;

    Serial.print("Sending message to topic1: ");
    Serial.println(topic1);
    Serial.println(dataT);

    Serial.print("Sending message to topic2: ");
    Serial.println(topic2);
    Serial.println(dataTemp);

    Serial.print("Sending message to topic3: ");
    Serial.println(topic3);
    Serial.println(dataH);

    Serial.print("Sending message to topic4: ");
    Serial.println(topic4);
    Serial.println(dataG);

    // send message, the Print interface can be used to set the message contents
    mqttClient.beginMessage(topic1);
    mqttClient.print(dataT);
    mqttClient.endMessage();

    mqttClient.beginMessage(topic2);
    mqttClient.print(dataTemp);
    mqttClient.endMessage();

    mqttClient.beginMessage(topic3);
    mqttClient.print(dataH);
    mqttClient.endMessage();

    mqttClient.beginMessage(topic4);
    mqttClient.print(dataG);
    mqttClient.endMessage();

    Serial.println();
  
  delay(1000);
  }
}
