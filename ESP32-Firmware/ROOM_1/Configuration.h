// #define mySSID "StaromiejskieKlimatyII"
// #define myPASSWORD "3264E937F"


// #define mqttServer "broker.hivemq.com"
// #define mqttPort 1883
// #define mqttUser "Saludos"
// #define mqttPassword ""

#define DAT_DHT22  15

//**    PWM latches parameters  
#define FREQUENCY 2048 
#define CHANNEL 0
#define RESOLUTION 8
#define buzzer_pin 10
#define motion_pin 23

#define LED_BUILDIN  2
#define MOTION_SENSOR_PIN 22
#define DOOR_SENSOR_PIN 23



#define TOPIC_TEMPERATURE  "DQReator/home/room1/Temperature"
#define TOPIC_HUMIDITY "DQReator/home/room1/Humidity"
#define TOPIC_MOTION "DQReator/home/room1/Motion"
#define TOPIC_LED "DQReator/home/room1/Ligth"
#define TOPIC_DOOR "DQReator/home/room1/Door"


#define DELAY_SENSORS 1000
