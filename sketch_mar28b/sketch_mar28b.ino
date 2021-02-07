/*
Arduino Neato XV-11 Motor control board v0.2 by Cheng-Lung Lee
Change log:
V0.2 Add simple speed control code update PWM 3 times per rev.
V0.1 Opend loop control version.

This code is tested on Arduino Mega 1280
I/O:
Motor drive by low side driver IPS041L connect to PWM Pin4, Motor power from 5V
Neato XV-11 LDS Vcc(red) : 5V
Neato XV-11 LDS TX(Orange) : RX3
 */


#include "lidar.h"

 void setup() {
    pinMode(MotorPWMPin, OUTPUT); 
    Serial.begin(115200);  // USB serial
    Serial3.begin(115200);  // XV-11 LDS data 

    // Pick your magic number and drive your motor , 178 is 178/255*5V=3.49V
    analogWrite(MotorPWMPin, DesiredRPM );  
}

void loop() {
  //speed of lidar unit
  analogWrite(MotorPWMPin, DesiredRPM ); 
  //read from lidar and write over bluetooh
   if (Serial3.available() > 0) {
    // get incoming byte:
    inByte = Serial3.read();
    Serial.write(inByte); 
    decodeData(inByte);
  }
}
