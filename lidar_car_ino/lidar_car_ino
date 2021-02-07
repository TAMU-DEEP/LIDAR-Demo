#include "lidar.h"
#include "car.h"

 void setup() {
    pinMode(MotorPWMPin, OUTPUT); 
    Serial.begin(115200);  // USB serial
    Serial3.begin(115200);  // XV-11 LDS data 

    // Pick your magic number and drive your motor , 178 is 178/255*5V=3.49V
    analogWrite(MotorPWMPin, DesiredRPM ); 

    //setup motor control
    pinMode(LED, OUTPUT); 
    pinMode(IN1,OUTPUT);
    pinMode(IN2,OUTPUT);
    pinMode(IN3,OUTPUT);
    pinMode(IN4,OUTPUT);
    pinMode(ENA,OUTPUT);
    pinMode(ENB,OUTPUT);
    stop();

    last_command_time =  millis();
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
    
   if (Serial.available() > 0){
      getstr = Serial.read();
      read_command();
      last_command_time =  millis();
    }
    //Stop car after 1 second
    current_time = millis();
    if (current_time-last_command_time > period) {
      stop();
      last_command_time =  millis();
    }
}
