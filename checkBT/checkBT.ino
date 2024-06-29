const int analogPin = A5; // 아날로그 핀 설정
const float R1 = 10000.0; // 저항 R1의 값 (10k ohms)
const float R2 = 10000.0; // 저항 R2의 값 (10k ohms)
const int numSamples = 10;

void setup() {
  Serial.begin(9600); // 시리얼 통신 시작
}

void loop() {
  float voltageSum = 0;
  for (int i = 0; i < numSamples; i++) {
    int analogValue = analogRead(analogPin); // 아날로그 핀 값 읽기
    float voltage = (analogValue / 1023.0) * 5.0; // 아날로그 값을 전압으로 변환
    voltageSum += voltage;
    delay(10); // 샘플 간 딜레이
  }

  float averageVoltage = voltageSum / numSamples;
  float batteryVoltage = averageVoltage * ((R1 + R2) / R2); // 실제 배터리 전압 계산
  float batteryLevel = getBatteryLevel(batteryVoltage);

  Serial.print(batteryVoltage);
  Serial.print(" ");
  Serial.println(batteryLevel);
  delay(1000); // 1초 대기
}

float getBatteryLevel(float voltage) {
  float minVoltage = 6.0;
  float maxVoltage = 8.4;
  if (voltage < minVoltage) return 0;
  if (voltage > maxVoltage) return 100;
  return (voltage - minVoltage) / (maxVoltage - minVoltage) * 100;
}
