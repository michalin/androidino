#ifndef TELEMETRIX_H
#define TELEMETRIX_H

#include <Arduino.h>

/* %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/
/*                    FEATURE ENABLING DEFINES                      */
/* %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/



// To disable a feature, comment out the desired enabling define or defines

// This will allow SPI support to be compiled into the sketch.
// Comment this out to save sketch space for the UNO
//#define SPI_ENABLED 1

// This will allow OneWire support to be compiled into the sketch.
// Comment this out to save sketch space for the UNO
//#define ONE_WIRE_ENABLED 1

// This will allow DHT support to be compiled into the sketch.
// Comment this out to save sketch space for the UNO
//#define DHT_ENABLED 1

// This will allow sonar support to be compiled into the sketch.
// Comment this out to save sketch space for the UNO
//#define SONAR_ENABLED 1

// This will allow servo support to be compiled into the sketch.
// Comment this out to save sketch space for the UNO
//#define SERVO_ENABLED 1

// This will allow stepper support to be compiled into the sketch.
// Comment this out to save sketch space for the UNO
//#define STEPPERS_ENABLED 1

// This will allow I2C support to be compiled into the sketch.
// Comment this out to save sketch space for the UNO
//#define I2C_ENABLED 1

#ifdef SERVO_ENABLED
#include <Servo.h>
#endif

#ifdef SONAR_ENABLED
#include <Ultrasonic.h>
#endif

#ifdef I2C_ENABLED
#include <Wire.h>
#endif

#ifdef DHT_ENABLED
#include <DHTStable.h>
#endif

#ifdef SPI_ENABLED
#include <SPI.h>
#endif

#ifdef ONE_WIRE_ENABLED
#include <OneWire.h>
#endif

#ifdef STEPPERS_ENABLED
#include <AccelStepper.h>
#endif


#define DEBUG_ENABLED 0

//Pins used by SoftwareSerial
#define RX_PIN 2
#define TX_PIN 3

#if DEBUG_ENABLED == 1
#include <SoftwareSerial.h>
extern SoftwareSerial DbgSerial;
#define DbgBegin(x) DbgSerial.begin(x)
#define DbgPrint(x) DbgBegin.print(x)
#define DbgPrintln(x) DbgSerial.println(x)
#else
#define DbgBegin(x)
#define DbgPrint(x)
#define DbgPrintln(x)
#endif

#define StdSerial Serial



extern void get_next_command();
define telemetrix_update() get_next_command()

extern void telemetrix_init();

extern void analogWrite_remote(uint8_t pin, int value);
extern void digitalWrite_remote(uint8_t pin, uint8_t value);
extern int digitalRead_remote(uint8_t pin);
extern int analogRead_remote(uint16_t pin);

extern void scan_digital_inputs();



#endif