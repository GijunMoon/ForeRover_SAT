#include <Arduino.h>
#include "global.h"
#include "main.h"
#include "motor.h"

void setup_() {
    Serial.begin(9600);
    motorSetup();
}

void loop_() {
    motorAForward(255); // 모터 A를 최고 속도로 전진
    delay(2000);       // 2초 대기
    motorABackward(255); // 모터 A를 최고 속도로 후진
    delay(2000);       // 2초 대기
    motorBForward(255); // 모터 B를 최고 속도로 전진
    delay(2000);       // 2초 대기
    motorBBackward(255); // 모터 B를 최고 속도로 후진
    delay(2000);       // 2초 대기
    motorStop();       // 모터 정지
    delay(2000);       // 2초 대기
}
