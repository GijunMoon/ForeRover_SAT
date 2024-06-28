import serial

port = 'COM13'
rate = 9600

ARD = serial.Serial(port, rate)

#전력 값 읽어들이는 코드 추가 checkBT.ino 참조!
#pyGUI 추가해서 그래프 그리는 기능 추가