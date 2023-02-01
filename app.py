import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from db import session
from send_mail import mail
from info import user,position,department
from login import Login
import time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from crud import create,get,update
# Base.metadata.create_all(bind=engine)


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self._db = next(session.get_db())
        while True:
            self.email,self.password= self.login_page()
            self.m = mail(self.email,self.password)
            self.mail = self.m.login_check()
            if self.mail==True:
                break
            s=QMessageBox.warning(self,'Login Check','로그인 실패',QMessageBox.Yes,QMessageBox.Yes)
        self.setupUI()
    
    def setupUI(self):
        self.setWindowTitle("서르 인력관리 프로그램")
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(),"images/logo.ico")))
        self.resize(1000,500)
        
        self.setMenuBar()        
        self.setting_widget()

    def login_page(self):
        Login_app = Login()
        Login_app.exec_()
        return Login_app.email,Login_app.password
        
    def setting_widget(self):
        widget = QWidget(self)
        self.Mainlayout = QVBoxLayout(widget)

        self.user_table()

        self.infolayout = QHBoxLayout()

        
        self.infolayout.addWidget(self.user_table)


        self.Mainlayout.addLayout(self.infolayout)

        
        self.setCentralWidget(widget)
    def user_table(self):
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(9)
        self.user_table.setHorizontalHeaderLabels(["","이름","사원번호","부서","직위","e-mail","입사일","퇴사일","기타"])
        self.user_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setting_table()

    def setting_table(self):    
        all_user = get.user_true(db= self._db)
        self.user_table.setRowCount(len(all_user))
        for i,user in enumerate(all_user):
            self.user_table.setCellWidget(i,0,QCheckBox())
            self.user_table.setItem(i,1,QTableWidgetItem(user.name))
            self.user_table.setItem(i,2,QTableWidgetItem(user.employee_number))
            self.user_table.setItem(i,3,QTableWidgetItem(user.department.department))
            self.user_table.setItem(i,4,QTableWidgetItem(user.position.position))
            self.user_table.setItem(i,5,QTableWidgetItem(user.email))
            self.user_table.setItem(i,6,QTableWidgetItem(user.join_date.strftime("%Y-%m-%d")))
            if user.resignation_date is None:
                self.user_table.setItem(i,7,QTableWidgetItem(""))
            else:
                self.user_table.setItem(i,7,QTableWidgetItem(user.resignation_date))
            if user.etc is None:
                self.user_table.setItem(i,8,QTableWidgetItem(""))
            else:
                self.user_table.setItem(i,8,QTableWidgetItem(user.etc))
            self.user_table.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeToContents)  
            self.user_table.horizontalHeader().setSectionResizeMode(8,QHeaderView.Stretch) 
        #self.user_table.resizeColumnsToContents()
        self.user_table.resizeRowsToContents()
            

    def add_user(self):
        add_user_app = user.Add_user(self.email)
        add_user_app.exec_()
        self.setting_table()

    def update_user(self):
        add_user_app = user.Update_user(self.email)
        add_user_app.exec_()
        self.setting_table()

    def add_department(self):
        add_department_app = department.Add_department()
        add_department_app.exec_()
 
    def update_department(self):
        add_department_app = department.Update_department()
        add_department_app.exec_()

    def add_position(self):
        add_position_app = position.Add_position()
        add_position_app.exec_()

    def update_position(self):
        add_position_app = position.Update_position()
        add_position_app.exec_()
        

    def setUsermenu(self):
        self.useraddaction = QAction("Add User",self)
        self.useraddaction.setStatusTip("Add a User")
        self.useraddaction.triggered.connect(self.add_user)

        self.userchangeaction = QAction("Change info",self)
        self.userchangeaction.setStatusTip("Change user information")
        self.userchangeaction.triggered.connect(self.update_user)

    def setDepartmentmenu(self):
        self.departmentaddaction = QAction("Add Department",self)
        self.departmentaddaction.setStatusTip("Add a Department")
        self.departmentaddaction.triggered.connect(self.add_department)

        self.departmentchangeaction = QAction("Change info",self)
        self.departmentchangeaction.setStatusTip("Change Department information")
        self.departmentchangeaction.triggered.connect(self.update_department)

    def setPositionmenu(self):
        self.positionaddaction = QAction("Add Position",self)
        self.positionaddaction.setStatusTip("Add a Position")
        self.positionaddaction.triggered.connect(self.add_position)

        self.positionchangeaction = QAction("Change info",self)
        self.positionchangeaction.setStatusTip("Change position information")
        self.positionchangeaction.triggered.connect(self.update_position)

    def setMenuBar(self):
        self.setUsermenu()
        self.setDepartmentmenu()
        self.setPositionmenu()

        self.statusBar()
        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)

        usermenu = self.menubar.addMenu('&User')
        usermenu.addAction(self.useraddaction)
        usermenu.addAction(self.userchangeaction)

        departmentmenu = self.menubar.addMenu('&Department')
        departmentmenu.addAction(self.departmentaddaction)
        departmentmenu.addAction(self.departmentchangeaction)

        positionmenu = self.menubar.addMenu('&Position')
        positionmenu.addAction(self.positionaddaction)
        positionmenu.addAction(self.positionchangeaction)
        

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())