import os
import sys
import serial
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtWidgets, QtCore, QtGui

# 시리얼 통신 설정
try:
    ser = serial.Serial('COM13', 9600)  # 아두이노와 연결된 포트 확인 (예: COM3)
except serial.SerialException as e:
    print(f"Could not open port: {e}")
    sys.exit(1)

class BatteryMonitorApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.x_data = []
        self.y_data_voltage = []
        self.y_data_level = []
        self.start_time = time.time()
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_graph)
        self.update_timer.start(1000)  # 1초마다 업데이트

    def initUI(self):
        self.setWindowTitle('Battery Monitor')

        main_layout = QtWidgets.QVBoxLayout()

        # 로고 추가
        logo_label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap("gui\logo.png")
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(logo_label)

        # 배터리 잔량 표시
        battery_layout = QtWidgets.QHBoxLayout()
        self.battery_label = QtWidgets.QLabel('Battery Level:')
        battery_layout.addWidget(self.battery_label)

        self.battery_progressbar = QtWidgets.QProgressBar()
        self.battery_progressbar.setOrientation(QtCore.Qt.Horizontal)
        self.battery_progressbar.setMaximum(100)
        battery_layout.addWidget(self.battery_progressbar)
        
        main_layout.addLayout(battery_layout)

        # 그래프 추가
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        main_layout.addWidget(self.canvas)

        self.setLayout(main_layout)
        self.show()

    def read_serial_data(self):
        if ser.in_waiting > 0:
            try:
                data = ser.readline().decode('utf-8').strip()
                battery_voltage, battery_level = map(float, data.split(' '))
                return battery_voltage, battery_level
            except ValueError:
                return None, None
        return None, None

    def update_gui(self):
        battery_voltage, battery_level = self.read_serial_data()
        if battery_voltage is not None and battery_level is not None:
            self.battery_progressbar.setValue(int(battery_level))  # float를 int로 변환
            print(f"Battery Voltage: {battery_voltage:.2f}V, Battery Level: {battery_level:.2f}%")

    def update_graph(self):
        battery_voltage, battery_level = self.read_serial_data()
        if battery_voltage is not None and battery_level is not None:
            current_time = time.time() - self.start_time
            self.x_data.append(current_time)
            self.y_data_voltage.append(battery_voltage)
            self.y_data_level.append(battery_level)

            # 그래프 업데이트
            self.ax.clear()
            self.ax.plot(self.x_data, self.y_data_voltage, 'r-', label='Voltage (V)')
            self.ax.plot(self.x_data, self.y_data_level, 'b-', label='Battery Level (%)')
            self.ax.set_xlabel('Time (s)')
            self.ax.set_ylabel('Value')
            self.ax.legend()

            self.canvas.draw()
            print(f"Battery Voltage: {battery_voltage:.2f}V, Battery Level: {battery_level:.2f}%")

        # GUI 업데이트 (Progress Bar)
        self.update_gui()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = BatteryMonitorApp()
    sys.exit(app.exec_())
