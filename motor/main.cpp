#include <Arduino.h>
#include "global.h"
#include "main.h"
#include "motor.h"

void setup_() {
    Serial.begin(9600);
    motorSetup();
}

void loop_() {
    if (Serial.available() > 0) {
    // 시리얼 데이터 읽기
        String command = Serial.readStringUntil('\n');
        command.trim(); // 공백 제거
    
    // 명령에 따른 동작 수행
    if (command == "F") {
        forward();
        Serial.println("전진!");
    } else if (command == "B") {
        backward();
        Serial.println("후진!");
    } else {
        Serial.println("Unknown command. Please use F or B.");
    }
    if (command == "S"){
        motorStop();
        Serial.println("정지");
    }
  }
    //motorAForward(255); // 모터 A를 최고 속도로 전진
    //delay(2000);       // 2초 대기
    //motorABackward(255); // 모터 A를 최고 속도로 후진
    //delay(2000);       // 2초 대기
    //motorBForward(255); // 모터 B를 최고 속도로 전진
    //delay(2000);       // 2초 대기
    //motorBBackward(255); // 모터 B를 최고 속도로 후진
    //delay(2000);       // 2초 대기
    //motorStop();       // 모터 정지
    //delay(2000);       // 2초 대기
}

void forward(){
    motorAForward(255);
    motorBForward(255);
}

void backward(){
    motorABackward(255);
    motorBBackward(255);
}
