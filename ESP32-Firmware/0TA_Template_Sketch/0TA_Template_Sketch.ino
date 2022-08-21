#define ESP32_RTOS  // Uncomment this line if you want to use the code with freertos only on the ESP32
#include "OTA.h"
#define mySSID "StaromiejskieKlimatyII"
#define myPASSWORD "3264E937F"

void setup() {
  Serial.begin(115200);
  Serial.println("Booting");
  setupOTA("TemplateSketch", mySSID, myPASSWORD);

  // Your setup code
}

void loop() {
#ifdef defined(ESP32_RTOS) && defined(ESP32)
#else // If you do not use FreeRTOS, you have to regulary call the handle method.
  ArduinoOTA.handle();
#endif

  // Your code here

}