import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QDate,Qt
from db import session
from crud import create,get


class Add_department(QDialog):
    def __init__(self):
        super().__init__()
        self._db = next(session.get_db())
        self.setupUI()


    def setupUI(self):
        self.setGeometry(1100, 200, 300, 100)
        self.setWindowTitle("부서 추가")
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(),"images/logo.ico")))

        name_label = QLabel("부서명: ")

        self.name_edit = QLineEdit()

        self.pushButton1 = QPushButton("추가")
        self.pushButton1.clicked.connect(self.pushButtonClicked)

        layout = QGridLayout()
        layout.addWidget(name_label, 0, 0)
        layout.addWidget(self.name_edit, 0, 1)
        layout.addWidget(self.pushButton1, 3, 2)
        
        self.setLayout(layout)


    
    @staticmethod
    def show_message(message):
        msg = QMessageBox()
        msg.setText(message)
        msg.exec_()

    def pushButtonClicked(self):
        self.department_name = self.name_edit.text()
        try:
            create.department(
                db=self._db,
                employee_number = self.department_name,
            )
            self.close()
        except:
            self.show_message("재시도")  
     