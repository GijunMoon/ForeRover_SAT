#include "global.h"
#include <SoftwareSerial.h>

SoftwareSerial bluetooth(RXD, TXD)

void setup_(){
    bluetooth.begin(9600);
}

void loop_(){
    if (bluetooth.available()){
        Serial.write(bluetooth.read());
    }
    if(Serial.available()){
        bluetooth.write(Serial.read()); //AT 입력시 ok 반환
    }
}