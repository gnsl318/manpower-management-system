import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QDate,Qt
from db import session
from crud import create,get,update,delete


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
        raw_position = self.position_box.currentText()
        position= self.position_label.text()
        try:
            result=update.position(
                db=self._db,
                raw_position=raw_position,
                position=position
            )
            if result ==True:
                self.close()
            else:
                s=QMessageBox.warning(self,'Position Update','수정실패',QMessageBox.Yes,QMessageBox.Yes)
        except Exception as e:
            print(e)

    def deleteButtonClicked(self):
        position = self.position_box.currentText()
        try:
            result = delete.position(
                db=self._db,
                position = position,
            )
            if result ==0:
                self.close()
            elif result ==1:
                s=QMessageBox.warning(self,'Position Delete','DB Error 개발팀 문의부탁드립니다.',QMessageBox.Yes,QMessageBox.Yes)
            elif result == 2:
                s=QMessageBox.warning(self,'Position Delete','해당 파트에 포함된 사람이 있습니다.',QMessageBox.Yes,QMessageBox.Yes)
        except Exception as e:
            print(e)
            s=QMessageBox.warning(self,'Position Delete','삭제실패',QMessageBox.Yes,QMessageBox.Yes)