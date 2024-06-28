#include "global.h"
#include <SoftwareSerial.h>
#include <Arduino.h>

SoftwareSerial bluetooth(RXD, TXD);

void setup_ble(){
    bluetooth.begin(9600);
}

void loop_ble(){
    if (bluetooth.available()){
        Serial.write(bluetooth.read());
    }
    if(Serial.available()){
        bluetooth.write(Serial.read()); //AT 입력시 ok 반환
    }
}