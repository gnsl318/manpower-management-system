import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QDate,Qt

class Login(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()


    def setupUI(self):
        self.setGeometry(1100, 200, 300, 100)
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon("icon.png"))
        
        
        id_label = QLabel("E-mail: ")
        self.id_edit = QLineEdit()
        
        password_label = QLabel("PASSWORD: ")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("로그인")
        self.login_btn.clicked.connect(self.pushButtonClicked)

        layout = QGridLayout()
        layout.addWidget(id_label, 0, 0)
        layout.addWidget(self.id_edit, 0, 1)
        layout.addWidget(password_label,1,0)
        layout.addWidget(self.password_edit,1,1)
        layout.addWidget(self.login_btn,2,1)
        self.setLayout(layout)
        
    @staticmethod
    def show_message(message):
        msg = QMessageBox()
        msg.setText(message)
        msg.exec_()

    def pushButtonClicked(self):
        self.email = self.id_edit.text()
        self.password = self.password_edit.text()
        self.close()
        return self.email, self.password
