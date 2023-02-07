import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QThread, pyqtSignal, QObject, pyqtSlot
from db import session
from send_mail import mail
from info import user,position,department,download
from login import Login
import time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from crud import create,get,update
# Base.metadata.create_all(bind=engine)

class MyThread(QThread):
    def __init__(self,info):
        super().__init__()
        self.info=info
    # Create a counter thread
    change_value = pyqtSignal(int)
    def run(self):
        cnt = 0
        while cnt<self.info:
            cnt+=1
            time.sleep(0.1)
            self.change_value.emit(cnt)
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
        self.resize(800,500)
        self.setMenuBar()        
        self.setting_widget()

    def login_page(self):
        Login_app = Login()
        Login_app.exec_()
        return Login_app.email,Login_app.password
        
    def setting_widget(self):
        widget = QWidget(self)
        self.Mainlayout = QVBoxLayout(widget)

        self.setUser_table()

        self.infolayout = QHBoxLayout()
        self.infolayout.addWidget(self.user_table)
        
        self.control_buttonlayout = QGridLayout()
        self.resignation_button = QPushButton("퇴사",self)
        self.resignation_button.clicked.connect(self.resignationButtonClicked)
        self.control_buttonlayout.addWidget(self.resignation_button,0,0,1,3)

        self.post_label = QLabel("급여명세서 발송 : ",self)
        self.post_label.setAlignment(Qt.AlignCenter)
        self.totalpost_button = QPushButton("전체발송",self)
        self.totalpost_button.clicked.connect(self.posttotal)
        self.selectpost_button = QPushButton("선택발송",self)

        self.selectpost_button.clicked.connect(self.postselect)
        self.control_buttonlayout.addWidget(self.post_label,1,0)
        self.control_buttonlayout.addWidget(self.selectpost_button,1,1)
        self.control_buttonlayout.addWidget(self.totalpost_button,1,2)




        self.Mainlayout.addLayout(self.infolayout)
        self.Mainlayout.addLayout(self.control_buttonlayout)


        
        self.setCentralWidget(widget)

    def posttotal(self):
        self.progressbar = QProgressBar()
        self.control_buttonlayout.addWidget(self.progressbar,2,0,1,3)
        self.folder_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        all_user = get.user_true(db= self._db)
        self.progressbar.setMaximum(len(all_user))
        self.thread = MyThread(len(all_user))
        self.thread.change_value.connect(self.setProgressVal)
        self.thread.start()
        self.thread.working=False
        for user in all_user:
            self.thread.working=True
            result = self.m.send_mail(folder_path=self.folder_path,email=user.email,name=user.name)
            create.post_log(db=self._db,user_name=user.name,result=str(result),post_user_email=self.email)
            self.thread.working=False

    def postselect(self):
        self.progressbar = QProgressBar()
        self.control_buttonlayout.addWidget(self.progressbar,2,0,1,3)
        self.folder_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.info={}
        for index,box in enumerate(self.checkbox_list):
            if box.isChecked():
                name = self.user_table.item(index,1).text()
                self.info[name]=self.user_table.item(index,5).text()
                box.setChecked(False)

        self.progressbar.setMaximum(len(self.info))
        self.thread = MyThread(len(self.info))
        self.thread.change_value.connect(self.setProgressVal)
        self.thread.start()
        self.thread.working=False
        for name,email in self.info.items():
            self.thread.working=True
            result =self.m.send_mail(folder_path=self.folder_path,email=email,name=name)
            create.post_log(db=self._db,user_name=user.name,result=str(result),post_user_email=self.email)
            self.thread.working=False

        
        
        #self.progressbar.setVisible(False)
    def setProgressVal(self, val):
        self.progressbar.setValue(val)
    


    def setUser_table(self):
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(6)
        self.user_table.setHorizontalHeaderLabels(["","이름","사원번호","부서","직위","e-mail"])#,"입사일","퇴사일","기타"])
        self.user_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setting_table()

    def resignationButtonClicked(self):
        name_list = []
        for index,box in enumerate(self.checkbox_list):
            if box.isChecked():
                name = self.user_table.item(index,1).text()
                name_list.append(name)
                box.setChecked(False)
        error_list = []
        for name in name_list:
            result = update.user_resignation(db=self._db,name=name,edit_user_email=self.email)
            if result ==False:
                error_list.append(name)
        if len(error_list)>=1:
            s=QMessageBox.warning(self,'Login Check',f'{error_list} 퇴사 실패' ,QMessageBox.Yes,QMessageBox.Yes)
        self.setting_table()



    def setting_table(self):    
        all_user = get.user_true(db= self._db)
        self.user_table.setRowCount(len(all_user))
        self.checkbox_list=[]
        for i,user in enumerate(all_user):
            ckbox = QCheckBox()
            self.user_table.setCellWidget(i,0,ckbox)
            self.checkbox_list.append(ckbox)
            self.user_table.setItem(i,1,QTableWidgetItem(user.name))
            self.user_table.setItem(i,2,QTableWidgetItem(user.employee_number))
            self.user_table.setItem(i,3,QTableWidgetItem(user.department.department))
            self.user_table.setItem(i,4,QTableWidgetItem(user.position.position))
            self.user_table.setItem(i,5,QTableWidgetItem(user.email))
            # self.user_table.setItem(i,6,QTableWidgetItem(user.join_date.strftime("%Y-%m-%d")))
            # if user.resignation_date is None:
            #     self.user_table.setItem(i,7,QTableWidgetItem(""))
            # else:
            #     self.user_table.setItem(i,7,QTableWidgetItem(user.resignation_date))
            # if user.etc is None:
            #     self.user_table.setItem(i,6,QTableWidgetItem(""))
            # else:
            #     self.user_table.setItem(i,6,QTableWidgetItem(user.etc))
            self.user_table.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeToContents)  
            self.user_table.horizontalHeader().setSectionResizeMode(5,QHeaderView.Stretch) 
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

    def download_user(self):
        download_app = download.Download_user()
        download_app.exec_()
    
    def download_log(self):
        download_app = download.Download_log()
        download_app.exec_()


        

    def setUsermenu(self):
        self.useraddaction = QAction("입사",self)
        self.useraddaction.setStatusTip("Add a User")
        self.useraddaction.triggered.connect(self.add_user)

        self.userchangeaction = QAction("사원 정보 변경",self)
        self.userchangeaction.setStatusTip("Change user information")
        self.userchangeaction.triggered.connect(self.update_user)

    def setDepartmentmenu(self):
        self.departmentaddaction = QAction("부서 추가",self)
        self.departmentaddaction.setStatusTip("Add a Department")
        self.departmentaddaction.triggered.connect(self.add_department)

        self.departmentchangeaction = QAction("부서명 변경",self)
        self.departmentchangeaction.setStatusTip("Change Department information")
        self.departmentchangeaction.triggered.connect(self.update_department)

    def setPositionmenu(self):
        self.positionaddaction = QAction("직위 추가",self)
        self.positionaddaction.setStatusTip("Add a Position")
        self.positionaddaction.triggered.connect(self.add_position)

        self.positionchangeaction = QAction("직위명 변경",self)
        self.positionchangeaction.setStatusTip("Change position information")
        self.positionchangeaction.triggered.connect(self.update_position)

    def setDownloadmenu(self):
        self.userdownloadaction = QAction("사원 정보",self)
        self.userdownloadaction.setStatusTip("User Infomation Download")
        self.userdownloadaction.triggered.connect(self.download_user)

        self.postdownloadaction = QAction("로그 기록",self)
        self.postdownloadaction.setStatusTip("Post Log Download")
        self.postdownloadaction.triggered.connect(self.download_log)


    def setMenuBar(self):
        self.setUsermenu()
        self.setDepartmentmenu()
        self.setPositionmenu()
        self.setDownloadmenu()

        self.statusBar()
        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)

        usermenu = self.menubar.addMenu('&인력')
        usermenu.addAction(self.useraddaction)
        usermenu.addAction(self.userchangeaction)

        departmentmenu = self.menubar.addMenu('&부서')
        departmentmenu.addAction(self.departmentaddaction)
        departmentmenu.addAction(self.departmentchangeaction)

        positionmenu = self.menubar.addMenu('&직위')
        positionmenu.addAction(self.positionaddaction)
        positionmenu.addAction(self.positionchangeaction)

        downloadmenu = self.menubar.addMenu('&Download')
        downloadmenu.addAction(self.userdownloadaction)
        downloadmenu.addAction(self.postdownloadaction)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())