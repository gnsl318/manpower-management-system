import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QDate,Qt
from db import session
from crud import create, get,update
import pandas as pd

def download(db,part,limit="total"):
    try:
        if part =="user":
            df = pd.DataFrame(columns=["사원번호","이름","부서","직위","e-mail","입사일","퇴사일","정보입력한 사람","기타"])
            if limit !="total":
                excel_name = "User_exist.xlsx"
                user_info = get.user_true(db=db) 
            else:
                excel_name = "User_Total.xlsx"
                user_info = get.user(db=db)
                        
            for index,user in enumerate(user_info):
                if user.name =="Admin":
                    continue
                if user.join_user ==None:
                    join_name =""
                else:
                    join_name = user.join_user.name
                df.loc[index] = [user.employee_number,user.name,user.department.department,user.position.position,user.email,str(user.join_date).split("+")[0],str(user.resignation_date).split("+")[0],join_name,user.etc]
            
        elif part =="user_log":
            df = pd.DataFrame(columns=["변경된 사원 이름","원본","변경","변경날짜","정보입력한 사람"])
            excel_name = "User_change_log.xlsx"
            user_logs = get.user_log(db=db)
            for index,log in enumerate(user_logs):
                df.loc[index] = [log.user.name,log.raw,log.change,str(log.change_date).split("+")[0],log.change_user.name]
        elif part =="post_log":
            df = pd.DataFrame(columns=["수신자명","발솔 날짜","결과","발송자명"])
            excel_name = "Post_log.xlsx"
            post_logs = get.post_log(db=db)
            for index,log in enumerate(post_logs):
                df.loc[index] = [log.user.name,str(log.post_date).split("+")[0],log.result,log.post_user.name]
        save_dir = os.path.abspath(os.getcwd())
        df.to_excel(os.path.join(save_dir,excel_name))
        return True
    except Exception as e:
        print(e)
        return False


        
    

class Download_user(QDialog):
    def __init__(self):
        super().__init__()
        self._db = next(session.get_db())
        self.setupUI()


    def setupUI(self):
        self.setGeometry(600, 600, 500, 100)
        self.resize(100,200)

        
        self.setWindowTitle("사원정보 다운로드")
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(),"images/logo.ico")))
        
        self.totalradioButton = QRadioButton('전체 인력', self)
        self.trueradioButton = QRadioButton('근무 중 인력', self)

        self.downloadButton = QPushButton("다운로드",self)
        self.downloadButton.clicked.connect(self.user_download)

        #self.radioButton.clicked.connect()

        layout = QGridLayout()
        layout.addWidget(self.totalradioButton,0,0)
        layout.addWidget(self.trueradioButton,0,1)
        layout.addWidget(self.downloadButton,1,0,1,2)
        self.setLayout(layout)


    def user_download(self):
        if self.totalradioButton.isChecked():
            result = download(self._db,"user","total")
        elif self.trueradioButton.isChecked():
            result = download(self._db,"user","limit")
        if result==True:
            self.close()
        else:
            s=QMessageBox.warning(self,'User info Download','다운로드 실패! 개발팀 문의부탁드립니다.',QMessageBox.Yes,QMessageBox.Yes)

class Download_log(QDialog):
    def __init__(self):
        super().__init__()
        self._db = next(session.get_db())
        self.setupUI()


    def setupUI(self):
        self.setGeometry(600, 600, 500, 100)
        self.resize(100,200)

        
        self.setWindowTitle("로그 다운로드")
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(),"images/logo.ico")))

        self.userradioButton = QRadioButton('유저 정보 변경 로그 ', self)
        self.postradioButton = QRadioButton('급여 명세서 발송 로그', self)

        self.downloadButton = QPushButton("다운로드",self)
        self.downloadButton.clicked.connect(self.log_download)

        #self.radioButton.clicked.connect()

        layout = QGridLayout()
        layout.addWidget(self.userradioButton,0,0)
        layout.addWidget(self.postradioButton,0,1)
        layout.addWidget(self.downloadButton,1,0,1,2)
        self.setLayout(layout)

    def log_download(self):
        if self.userradioButton.isChecked():
            result = download(self._db,"user_log")
        elif self.postradioButton.isChecked():
            result = download(self._db,"post_log")
        if result==True:
            self.close()
        else:
            s=QMessageBox.warning(self,'Log Download','다운로드 실패! 개발팀 문의부탁드립니다.',QMessageBox.Yes,QMessageBox.Yes)