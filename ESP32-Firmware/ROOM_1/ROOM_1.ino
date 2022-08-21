#include <WiFi.h>
#include <PubSubClient.h>
#include "Configuration.h"
#include "DHTesp.h"
#include "Ticker.h"


// #define DEBUG_VALUES
#define DEBUG_DOOR
#define DEBUG_MOTION
#define DEBUG_LED


// WiFi
const char* ssid = "toya47625627";
const char* password =  "g00MPh0k6K";
const int mqttPort = 1883;


// MQTT Broker
const char *mqtt_broker = "broker.hivemq.com";
const char* mqtt_username = "Saludos";
const char* mqtt_password = "public";
const int mqtt_port = 1883;
const char *topic = "DQReator/home/room1/LigthC";

WiFiClient espClient;
PubSubClient client(espClient);

// Temperature sensor
/** Initialize DHT sensor 1 */
DHTesp dhtSensor1;
//>>TASK HANDLERS
/** Task handle for the dht sensor reading*/
TaskHandle_t tempTaskHandle = NULL;
/** Flags for temperature dht readings finished */
bool gotNewTemperature = false;
/** Ticker for temperature dht reading */
Ticker tempTicker;
/** Data from sensor dht */
TempAndHumidity sensor1Data;
/* Flag if main loop is running */
bool tasksEnabled = false;

//VARIABLES DATA 
float tempDHT = 0.0;
float humidity = 0.0;
char humstring[8];
char tempstring[8];

bool motion_status = LOW;
bool motion_status_last = motion_status;

bool led_status = LOW;
bool led_status_last = led_status;

bool door_status = LOW;
bool door_status_last = door_status;

void setup() {
  // Set software serial baud to 115200;
  Serial.begin(115200);

  // Set I/O
  pinMode(LED_BUILDIN, OUTPUT);
  pinMode(DOOR_SENSOR_PIN,INPUT);

  // Connecting to a WiFi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
      vTaskDelay(500 / portTICK_PERIOD_MS);
      Serial.println("CONNECTING WI-FI..");
  }
  Serial.println("-------->CONNECTION SUCCESFULLY");

  // Connecting to a mqtt broker
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);

  while (!client.connected()) {
      String client_id = "esp32-client-";
      client_id += String(WiFi.macAddress());
      Serial.printf("The client %s connects to the public mqtt broker\n", client_id.c_str());
      if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
          Serial.println("Public emqx mqtt broker connected");
      } else {
          Serial.print("failed with state ");
          Serial.print(client.state());
          vTaskDelay(2000 / portTICK_PERIOD_MS);
      }
 }
 // publish and subscribe
 client.publish(topic, "Hi, I'm ESP32 room 1");
 client.subscribe(topic);
//Configuration Humidity sensor
  dhtSensor1.setup(DAT_DHT22, DHTesp::DHT22);

  // Start task to get temperature
  xTaskCreatePinnedToCore(
          tempTask,             /* Function to implement the task */
          "tempTask ",          /* Name of the task */
          1024,                 /* Stack size in words */
          NULL,                 /* Task input parameter */
          2,                    /* Priority of the task */
          &tempTaskHandle,      /* Task handle. */
          1);   

    if (tempTaskHandle == NULL) {
        Serial.println("[ERROR] Failed to start task for temperature update");
    } else {
    // Start update of environment data every 30 seconds
        tempTicker.attach(4, triggerGetTemp);
        Serial.println("Reading");
    }

  // Signal end of setup() to tasks
  tasksEnabled = true;
}



void loop() {
  client.loop();
     /**Check and Send Temperature and Humidity**/
  if (gotNewTemperature) {
    tempDHT = sensor1Data.temperature;
    humidity = sensor1Data.humidity;
    gotNewTemperature = false;
    dtostrf(humidity, 1, 2, humstring);
    dtostrf(tempDHT, 1, 2, tempstring);
    #ifdef DEBUG_VALUES
      Serial.print("Humidity: "); Serial.println(humstring);
      Serial.print("Temperature: "); Serial.println(tempstring);
    #endif

    client.publish(TOPIC_TEMPERATURE,tempstring);
    client.publish(TOPIC_HUMIDITY,humstring);
  }
    /**Check and Send status of the motion sensor**/
  motion_status = digitalRead(MOTION_SENSOR_PIN);
  if(motion_status!=motion_status_last && motion_status == HIGH){
    #ifdef DEBUG_MOTION
    Serial.print("MOTION SENSOR ON\r\n");
    #endif
    client.publish(TOPIC_MOTION,"1");
    motion_status_last = motion_status;
  }else  if(motion_status!=motion_status_last && motion_status == LOW){
    #ifdef DEBUG_MOTION
    Serial.print("MOTION SENSOR OFF\r\n");
    #endif
    client.publish(TOPIC_MOTION,"0");
    motion_status_last = motion_status;
  }
  else{motion_status_last = motion_status;}

    /**Check and Send status of the led**/
  led_status = digitalRead(LED_BUILDIN);
  if(led_status!=led_status_last && led_status == HIGH){
    #ifdef DEBUG_LED
    Serial.print("LED ON\r\n");
    #endif
    client.publish(TOPIC_LED,"1");
    led_status_last = led_status;
  }else  if(led_status!=led_status_last && led_status == LOW){
    #ifdef DEBUG_LED
    Serial.print("LED OFF\r\n");
    #endif
    client.publish(TOPIC_LED,"0");
    led_status_last = led_status;
  }
  else{led_status_last = led_status;}

    /**Check and Send status of the door sensor**/
  door_status = digitalRead(DOOR_SENSOR_PIN);
  if(door_status!=door_status_last && door_status == HIGH){
    #ifdef DEBUG_DOOR
    Serial.print("DOOR CLOSED\r\n");
    #endif
    client.publish(TOPIC_DOOR,"0");
    door_status_last = door_status;
  }else  if(door_status!=door_status_last && door_status == LOW){
    #ifdef DEBUG_DOOR
    Serial.print("DOOR OPEN\r\n");
    #endif
    client.publish(TOPIC_DOOR,"1");
    door_status_last = door_status;
  }
  else{door_status_last = door_status;}

  vTaskDelay(DELAY_SENSORS / portTICK_PERIOD_MS);
}

//Tasks to keep reading the temperature from DHT
void tempTask(void *pvParameters) {
  Serial.println("tempTask loop started");
  while (1) // tempTask loop
  {
    if (tasksEnabled && !gotNewTemperature) { // Read temperature only if old data was processed already
      // Reading temperature for humidity takes about 250 milliseconds!
      // Sensor readings may also be up to 2 seconds 'old' (it's a very slow sensor)
      sensor1Data = dhtSensor1.getTempAndHumidity();  // Read values from sensor 1
      gotNewTemperature = true;
    }
    vTaskSuspend(NULL);
  }
}

void triggerGetTemp() {
  if (tempTaskHandle != NULL) {
     xTaskResumeFromISR(tempTaskHandle);
  }
}

void callback(char *topic, byte *payload, unsigned int length) {
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
      Serial.print((char) payload[i]);
  }
  Serial.println();
  Serial.println("-----------------------");
  digitalWrite(LED_BUILDIN, !digitalRead(LED_BUILDIN));
}