import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QDate,Qt
from db import session
from crud import create,get,update


class Add_position(QDialog):
    def __init__(self):
        super().__init__()
        self._db = next(session.get_db())
        self.setupUI()


    def setupUI(self):
        self.setGeometry(1100, 200, 300, 100)
        self.setWindowTitle("직위 추가")
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(),"images/logo.ico")))
        
    

        self.layout = QGridLayout()
        self.layout.addWidget(QLabel("직위명 : "),0,0)
        self.position_label = QLineEdit()
        self.layout.addWidget(self.position_label,0,1)

        self.pushButton = QPushButton("추가")
        self.pushButton.clicked.connect(self.pushButtonClicked)

        self.layout.addWidget(self.pushButton, 1, 2)
        
        self.setLayout(self.layout)


    def pushButtonClicked(self):
        self.position_name = self.position_label.text()
        try:
            create.department(
                db=self._db,
                department = self.position_name,
            )
            self.close()
        except:
            s=QMessageBox.warning(self,'Add Position','실패! 재시도해주세요',QMessageBox.Yes,QMessageBox.Yes) 
     
class Update_position(QDialog):
    def __init__(self):
        super().__init__()
        self._db = next(session.get_db())
        self.setupUI()


    def setupUI(self):
        self.setGeometry(600, 600, 500, 100)
        self.resize(300,100)

        self.set_searchbox()

        self.layout = QGridLayout()
        self.layout.addWidget(QLabel("직위명 : "),0,0)
        self.layout.addWidget(self.position_box,0,1)

        self.layout.addWidget(QLabel("변경명 : "),1,0)
        self.position_label = QLineEdit()
        self.layout.addWidget(self.position_label,1,1)


        self.update_button = QPushButton("저장")
        self.update_button.clicked.connect(self.updateButtonClicked)
        self.layout.addWidget(self.update_button,3,0,1,2)

        self.setLayout(self.layout)

    def set_searchbox(self):
        self.position_box = QComboBox()
        self.box_additem()

    def box_additem(self):
        position_info=get.position(db=self._db)

        for position in position_info:
            if position.position=="admin":
                self.position_box.addItem("Select")
                continue
            self.position_box.addItem(position.position)

    def updateButtonClicked(self):
        position= self.position_label.text()
        try:
            result=True
            if result ==True:
                self.close()
            else:
                s=QMessageBox.warning(self,'Position Update','수정실패',QMessageBox.Yes,QMessageBox.Yes)
        except Exception as e:
            print(e)
        