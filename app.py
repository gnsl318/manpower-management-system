import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from db import session
from crud import create,get
from send_mail import mail
from add_user import *
from add_department import *
from add_position import *
from login import Login
import time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

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
        self.setupUI()
    
    def setupUI(self):
        self.setWindowTitle("서르 인력관리 프로그램")
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(),"images/logo.ico")))
        self.resize(1000,500)
        
        self.setToolBar()        
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

        
        # self.edit_state_button = QPushButton("퇴사")
        # self.edit_state_button.clicked.connect(self.out)
        # self.up_button = QPushButton("▲")
        # self.up_button.clicked.connect(self.down_name)
        # self.down_button = QPushButton("▼")
        # self.down_button.clicked.connect(self.up_name)
        # # self.download_button = QPushButton("download")
        # self.send_button = QPushButton("발송")
        # self.send_button.clicked.connect(self.send)
        # self.all_send_button = QPushButton("전체발송")
        # self.all_send_button.clicked.connect(self.send_all)

        self.infolayout.addWidget(self.user_table)
        # self.infolayout.addWidget(self.name_box)
        # self.infolayout.addWidget(self.employee_number_label)
        # self.infolayout.addWidget(self.edit_state_button)
        # self.buttonlayout.addWidget(self.up_button)
        # self.buttonlayout.addWidget(self.down_button)
        # # self.buttonlayout.addWidget(self.download_button)
        # self.sendlayout.addWidget(self.send_button)
        # self.sendlayout.addWidget(self.all_send_button)

        self.Mainlayout.addLayout(self.infolayout)
        # self.Mainlayout.addLayout(self.buttonlayout)
        # self.Mainlayout.addLayout(self.sendlayout)
        
        self.setCentralWidget(widget)
    def user_table(self):
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(9)
        self.user_table.setHorizontalHeaderLabels(["","이름","사원번호","부서","직위","e-mail","입사일","퇴사일","기타"])

        self.user_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        all_user = get.all_user(db= self._db)
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
            


    # def send(self):
    #     name=self.name_box.currentText()
    #     employee_number = self.employee_number
    #     try:
    #         user_email = get_email(db=self._db,name=name,employee_number=employee_number).email
    #         self.m.send_mail(user_email,name)
    #     except:
    #         pass

    # def send_all(self):
    #     all_user = get_user(db= self._db)
    #     for user in all_user:
    #         try:
    #             self.m.send_mail(user.email,user.name)           
    #         except:
    #             pass
    # def out(self):
    #     update_state(db=self._db,employee_number=self.employee_number_label.text())
    #     self.name_box.clear()
    #     self.name_box_additem()

    # def up_name(self):
    #     index = self.name_box.currentIndex()
    #     if self.name_box.count()-1 == index:
    #         pass
    #     else:
    #         index +=1
    #         self.name_box.setCurrentIndex(index)
    # def down_name(self):
    #     index = self.name_box.currentIndex()
    #     if index == 0:
    #         pass
    #     else:
    #         index -=1
    #         self.name_box.setCurrentIndex(index)
        

    # def make_name_box(self):
    #     self.name_box = QComboBox()
    #     self.employee_number_label = QLabel()
    #     self.name_box_additem()
    
    # def set_employee_number_label(self):
    #     self.employee_number = get_employee_number(db=self._db,name =self.name_box.currentText())
    #     self.employee_number_label.setText(self.employee_number)

    # def name_box_additem(self):
    #     User_info=get_user(db=self._db)
    #     for user_name in User_info:
    #         self.name_box.addItem(user_name.name)
    #     self.set_employee_number_label()


    
    def add_user(self):
        add_user_app = Add_user(self.email)
        add_user_app.exec_()
        self.setupUI()

    def add_department(self):
        add_department_app = Add_department()
        add_department_app.exec_()
        self.setupUI()   

    def add_position(self):
        add_position_app = Add_position()
        add_position_app.exec_()
        self.setupUI()

    def setToolBar(self):
        self.statusBar()
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)
        self.add_user_button = QAction("Add_User",self)
        self.add_department_button = QAction("Add_Department",self)
        self.add_position_button = QAction("Add_Position",self)

        #self.add_user_button.setShortcut('Ctrl+A')
        self.add_user_button.triggered.connect(self.add_user)
        self.add_department_button.triggered.connect(self.add_department)
        self.add_position_button.triggered.connect(self.add_position)
        self.toolbar.addAction(self.add_user_button)
        self.toolbar.addAction(self.add_department_button)
        self.toolbar.addAction(self.add_position_button)
        

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())