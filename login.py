import configparser
import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QLineEdit, QMainWindow, QMessageBox,
                             QWidget)

import src.auto
import src.login_ui


class LoginUi(QWidget):
    def __init__(self):
        self.ui = src.login_ui.Ui_Form()
        super().__init__()
        self.ui.setupUi(self)
        self.ui.pw.setEchoMode(QLineEdit.EchoMode.Password)
        self.ui.close.clicked.connect(self.close)
        self.ui.Login.clicked.connect(self.login)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.show()

    def login(self):
        user = self.ui.usr.text().upper()
        pw = self.ui.pw.text().upper()
        if not user or not pw:
            return
        if user == 'PW' and pw == 'ILIKELIKE':
            self.hide()
            dist_dir = os.path.dirname(os.path.abspath(__file__))
            settings = configparser.ConfigParser()
            settings.read(os.path.join(dist_dir, './conf/main.ini'))
            if 'Window' in settings:
                window_settings = settings['Window']
                x = int(window_settings['x'])
                y = int(window_settings['y'])
                width = int(window_settings['width'])
                height = int(window_settings['height'])
                size = eval(window_settings['size'])
                save_path = window_settings['save_path']
                win = src.auto.ChatApp(size, save_path)
                win.setGeometry(x, y, width, height)
            else:
                win = src.auto.ChatApp([300, 120], None)
        else:
            QMessageBox.information(self, 'Info', 'Wrong password.')


if __name__ == '__main__':
    winstate = False
    app = QApplication([])
    window = LoginUi()

    app.exec()
