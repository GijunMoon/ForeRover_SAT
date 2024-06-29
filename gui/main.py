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
        self.last_voltage = None  # 마지막 전압 값을 저장할 변수
        self.last_change_time = None  # 마지막 전압 변화 시간을 저장할 변수
        self.start_time = time.time()
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_graph)
        self.update_timer.start(1000)  # 1초마다 업데이트

    def initUI(self):
        self.setWindowTitle('Battery Monitor')

        main_layout = QtWidgets.QVBoxLayout()

        # 로고 추가
        logo_label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap("gui/logo.png")
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

        # 명령 표시 레이블
        self.command_label = QtWidgets.QLabel('Current Command: None')
        main_layout.addWidget(self.command_label)

        # 전압 변화 시간 표시 레이블
        self.change_time_label = QtWidgets.QLabel('Last Voltage Change Time: None')
        main_layout.addWidget(self.change_time_label)

        # 그래프 추가
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        main_layout.addWidget(self.canvas)

        # 버튼 추가
        button_layout = QtWidgets.QGridLayout()
        
        self.forward_button = QtWidgets.QPushButton('전진')
        self.forward_button.clicked.connect(lambda: self.send_command('전진'))
        button_layout.addWidget(self.forward_button, 0, 1)
        
        self.backward_button = QtWidgets.QPushButton('후진')
        self.backward_button.clicked.connect(lambda: self.send_command('후진'))
        button_layout.addWidget(self.backward_button, 2, 1)
        
        self.left_button = QtWidgets.QPushButton('좌측')
        self.left_button.clicked.connect(lambda: self.send_command('좌측'))
        button_layout.addWidget(self.left_button, 1, 0)
        
        self.right_button = QtWidgets.QPushButton('우측')
        self.right_button.clicked.connect(lambda: self.send_command('우측'))
        button_layout.addWidget(self.right_button, 1, 2)
        
        self.stop_button = QtWidgets.QPushButton('정지')
        self.stop_button.clicked.connect(lambda: self.send_command('정지'))
        button_layout.addWidget(self.stop_button, 1, 1)
        
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.show()

    def read_serial_data(self):
        if ser.in_waiting > 0:
            try:
                data = ser.readline().decode('utf-8').strip()
                if data in ['전진', '후진']:
                    self.command_label.setText(f'Current Command: {data}')
                else:
                    battery_voltage, battery_level = map(float, data.split(' '))
                    return battery_voltage, battery_level
            except ValueError as e:
                print(f"Error reading serial data: {e}")
                return None, None
        return None, None

    def update_graph(self):
        battery_voltage, battery_level = self.read_serial_data()
        if battery_voltage is not None and battery_level is not None:
            current_time = time.time() - self.start_time
            self.x_data.append(current_time)
            self.y_data_voltage.append(battery_voltage)

            # 전압 변화 감지
            if self.last_voltage is not None and self.last_voltage != battery_voltage:
                self.last_change_time = current_time
                self.change_time_label.setText(f'전압 변화 시간: {current_time:.2f} s')

            self.last_voltage = battery_voltage

            # 그래프 업데이트
            self.ax.clear()
            self.ax.plot(self.x_data, self.y_data_voltage, 'r-', label='Voltage (V)')
            self.ax.set_xlabel('Time (s)')
            self.ax.set_ylabel('Voltage (V)')
            self.ax.legend()
            self.ax.set_ylim(0, 10)  # 세로축 범위를 0에서 10으로 설정

            self.canvas.draw()
            print(f"Battery Voltage: {battery_voltage:.2f}V, Battery Level: {battery_level:.2f}%")

            # GUI 업데이트 (Progress Bar)
            self.battery_progressbar.setValue(int(battery_level))  # float를 int로 변환

    def send_command(self, command):
        try:
            ser.write(f'{command}\n'.encode('utf-8'))
            self.command_label.setText(f'Current Command: {command}')
        except serial.SerialException as e:
            print(f"Error sending command: {e}")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = BatteryMonitorApp()
    sys.exit(app.exec_())
