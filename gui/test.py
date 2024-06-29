import os
import sys
from PyQt5.QtCore import QCoreApplication

# Qt 플러그인 경로 설정
plugin_path = os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages", "PyQt5", "Qt", "plugins")
QCoreApplication.setLibraryPaths(["C:\Users\문기준\AppData\Local\Programs\Python\Python310\Lib\site-packages\PyQt5\Qt5\plugins\platforms"])

from PyQt5.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
label = QLabel('Hello, PyQt5!')
label.show()
sys.exit(app.exec_())
