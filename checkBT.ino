const int analogPin = A0; // 전압 분배기에서 들어오는 아날로그 핀
const float R1 = 100000.0; // 전압 분배기의 첫 번째 저항 (단위: Ω)
const float R2 = 100000.0; // 전압 분배기의 두 번째 저항 (단위: Ω)
const float referenceVoltage = 5.0; // 아두이노의 참조 전압 (단위: V)

void setup() {
  Serial.begin(9600); // 시리얼 통신 시작
}

void loop() {
  int sensorValue = analogRead(analogPin); // 아날로그 핀에서 값 읽기
  float voltage = sensorValue * (referenceVoltage / 1023.0); // 센서 값을 전압으로 변환
  float batteryVoltage = voltage * ((R1 + R2) / R2); // 실제 배터리 전압 계산

  float batteryLevel = getBatteryLevel(batteryVoltage);

  Serial.print("Battery Voltage: ");
  Serial.print(batteryVoltage);
  Serial.print(" V, Battery Level: ");
  Serial.print(batteryLevel);
  Serial.println(" %");

  delay(1000); // 1초 대기
}

float getBatteryLevel(float voltage) {
  float minVoltage = 6.0; // 최소 전압 (방전 상태)
  float maxVoltage = 8.4; // 최대 전압 (완전 충전 상태)

  // 전압 범위를 잔량 퍼센트로 변환
  float batteryLevel = ((voltage - minVoltage) / (maxVoltage - minVoltage)) * 100.0;
  if (batteryLevel < 0) batteryLevel = 0;
  if (batteryLevel > 100) batteryLevel = 100;

  return batteryLevel;
}
