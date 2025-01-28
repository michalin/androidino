#include <Adafruit_NeoPixel.h>
#include"telemetrix.h"

#define WS2812_DIN 12

#define NUM_LEDS 1

//Analog values representing colors
#define RED 25
#define GREEN 25
#define BLUE 25

//Boundaries for distance
#define D_RED 0
#define D_YELLOW 10
#define D_GREEN 20
#define D_BLUE 40

#define TRIG_PIN  4
#define ECHO_PIN  5

#define TORCH_BTN_PIN 9  // Physical pin for torch button
#define TORCH_LED_PIN 11
#define TORCH_APP_BTN_VPIN 21 // Virtual pin for app torch button
#define LED_STATE_VPIN 22 // Virtual pin for torch LED state (on/off)
#define BRIGHTNESS_VPIN 23 // Virtual pin for torch LED brightness

#define DISTANCE_VPIN 10

unsigned long duration, distance;

Adafruit_NeoPixel led = Adafruit_NeoPixel(NUM_LEDS, WS2812_DIN, NEO_RGB + NEO_KHZ800);

void setup() {
  StdSerial.begin(115200);
  DbgBegin(115200);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  pinMode(WS2812_DIN, OUTPUT);
  pinMode(TORCH_BTN_PIN, INPUT_PULLUP);
  pinMode(TORCH_LED_PIN, OUTPUT);
  
  led.begin();
  led.show();
  telemetrix_init();
  //DbgPrintln("Setup done: " + String(digitalPinToPort(50)));
}

bool subscribed;

void loop() {
  telemetrix_update();
  
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  duration = pulseIn(ECHO_PIN, HIGH);
  distance = ((float)duration * .0343) / 2;
  
  analogWrite_remote(DISTANCE_VPIN, distance); //Send distance to the client

  //delay(10);
  if (distance < D_YELLOW) {  //Red range
      led.setPixelColor(0, RED, 0, 0); 
  } else if (distance >= D_YELLOW & distance < D_GREEN) {  //Yellow range
      led.setPixelColor(0, RED, GREEN, 0);

  } else if (distance >= D_GREEN & distance < D_BLUE) {  //Green range
      led.setPixelColor(0, 0, GREEN, 0); 

  } else if (distance >= D_GREEN) {  //Blue range
      led.setPixelColor(0, 0, 0, BLUE); 
  }
  led.show(); 

  // Toggle torch
  static bool torchOn = false;
  static uint8_t lastAppBtnState, lastBtnState;
  static int lastBrightness;
  static int pwmValue = 255;

  bool btnState = !digitalRead(TORCH_BTN_PIN);
  bool btnPressed = btnState & !lastBtnState;
  lastBtnState = btnState;
  
  bool appBtnState = digitalRead_remote(TORCH_APP_BTN_VPIN);
  bool appBtnPressed = appBtnState != lastAppBtnState;
  lastAppBtnState = appBtnState;
  
  int brightness =  analogRead_remote(BRIGHTNESS_VPIN);
  bool Brightness_canged = brightness != lastBrightness;
  lastBrightness = brightness;

  if (btnPressed)
  {
    DbgPrintln("btnPressed: " + String(btnPressed));
    torchOn = !torchOn;
    analogWrite(TORCH_LED_PIN, torchOn? pwmValue : 0);
    digitalWrite_remote(LED_STATE_VPIN, torchOn);
  }

  if (appBtnPressed)
  {
    DbgPrintln("appBtnPressed: " + String(appBtnPressed));
    torchOn = appBtnState;
    analogWrite(TORCH_LED_PIN, torchOn? pwmValue : 0);
  }

  if (Brightness_canged)
  {
    pwmValue = brightness; 
    analogWrite(TORCH_LED_PIN, torchOn? pwmValue : 0);
  }
}
 
