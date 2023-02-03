import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QDate,Qt
from db import session
from crud import create, get,update

class Add_user(QDialog):
    def __init__(self,email):
        super().__init__()
        self.email=email
        self._db = next(session.get_db())
        self.setupUI()


    def setupUI(self):
        self.setGeometry(600, 600, 500, 100)
        self.resize(600,300)
        self.add_user_table = QTableWidget()
        self.table_setting()
        self.setWindowTitle("사원추가")
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(),"images/logo.ico")))

        self.add_button = QPushButton("추가")
        self.add_button.clicked.connect(self.addButtonClicked)
        self.save_button = QPushButton("저장")
        self.save_button.clicked.connect(self.saveButtonClicked)
        layout = QHBoxLayout()
        layout.addWidget(self.add_user_table)
        layout.addWidget(self.add_button)
        layout.addWidget(self.save_button)
        

        self.setLayout(layout)
    def table_setting(self):
        self.add_user_table.setColumnCount(5)
        self.add_user_table.setRowCount(1)
        self.add_user_table.setHorizontalHeaderLabels(["이름","사원번호","부서","직위","e-mail"])
        self.add_user_table.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.add_user_table.resizeRowsToContents()
        for i in range(5):
            self.add_user_table.horizontalHeader().setSectionResizeMode(i,QHeaderView.Stretch)
        #self.add_user_table.resizeColumnsToContents()


    def addButtonClicked(self):
        rowPosition = self.add_user_table.rowCount()
        try:
            self.add_user_table.insertRow(rowPosition)
        except:
            self.show_message("재시도")

    def saveButtonClicked(self):
        row_count = self.add_user_table.rowCount()
        col_count = self.add_user_table.columnCount()
        result_list = []
        for i in range(row_count):
            user_info = []
            try:
                for j in range(col_count):
                    user_info.append(self.add_user_table.item(i,j).text())
            except:
                continue
            try:
                result = create.user(
                    db=self._db,
                    name = user_info[0],
                    employee_number = user_info[1],
                    department = user_info[2],
                    position = user_info[3],
                    email = user_info[4],
                    join_user = self.email
                )
                if result != False:
                    result_list.append(result)
                self.close()
            except:
                continue
        self.show_message(result_list)

class Update_user(QDialog):
    def __init__(self,email):
        super().__init__()
        self.email=email
        self._db = next(session.get_db())
        self.setupUI()


    def setupUI(self):
        self.setGeometry(600, 600, 500, 100)
        self.resize(300,100)

        self.set_searchbox()

        self.layout = QGridLayout()
        self.layout.addWidget(QLabel("부서 : "),0,0)
        self.layout.addWidget(self.department_box,0,1)
        self.layout.addWidget(QLabel("직위 : "),1,0)
        self.layout.addWidget(self.position_box,1,1)

        self.serch_button = QPushButton("검색")
        self.serch_button.clicked.connect(self.searchButtonClicked)
        self.layout.addWidget(self.serch_button,3,0,1,2)

        self.setLayout(self.layout)

    def set_searchbox(self):
        self.department_box = QComboBox()
        self.position_box = QComboBox()
        self.box_additem()

    def box_additem(self):
        department_info=get.department(db=self._db)
        position_info=get.position(db=self._db)

        for department in department_info:
            if department.department=="admin":
                self.department_box.addItem("Select")
                continue
            self.department_box.addItem(department.department)
        for position in position_info:
            if position.position=="admin":
                self.position_box.addItem("Select")
                continue
            self.position_box.addItem(position.position)

    def set_user_info(self):
        name=self.search_box.currentText()
        self.employee_number_label = QLineEdit(self.user_dic[name].employee_number,self)
        self.employee_number_label.setReadOnly(True)
        self.name_label = QLineEdit(self.user_dic[name].name,self)
        self.department_label = QLineEdit(self.user_dic[name].department.department,self)
        self.position_label = QLineEdit(self.user_dic[name].position.position,self)
        self.email_label = QLineEdit(self.user_dic[name].email,self)
        if name != "Select":
            self.layout.addWidget(self.employee_number_label,6,1)
            self.layout.addWidget(self.name_label,7,1)
            self.layout.addWidget(self.department_label,8,1)
            self.layout.addWidget(self.position_label,9,1)
            self.layout.addWidget(self.email_label,10,1)
            self.saveUpdateButton = QPushButton("저장")
            self.saveUpdateButton.clicked.connect(self.updateButtonClicked)
            self.layout.addWidget(self.saveUpdateButton,11,1)
        else:
            pass
    @staticmethod
    def show_message(message):
        msg = QMessageBox()
        msg.setText(message)
        msg.exec_()
    
    def searchButtonClicked(self):
        department = self.department_box.currentText()
        position = self.position_box.currentText()
        if department !="Select" and position != "Select":
            user_info = get.user_dep_pos(db=self._db,department=department,position=position)
        elif department !="Select" and position == "Select":
            user_info = get.user_department(db=self._db,department=department)
        elif department =="Select" and position != "Select":
            user_info = get.user_position(db=self._db,position=position)
        else:
            user_info = get.user(db=self._db)
        self.search_box = QComboBox()
        self.user_dic={}
        self.search_box.addItem("Select")
        for user in user_info:
            if user.name=="Admin":
                continue
            self.user_dic[user.name]=user
            self.search_box.addItem(user.name)
        
        self.layout.addWidget(self.search_box,4,0,1,2)
        self.layout.addWidget(QLabel("사원번호 : "),6,0)
        self.layout.addWidget(QLabel("이름 : "),7,0)
        self.layout.addWidget(QLabel("부서 : "),8,0)
        self.layout.addWidget(QLabel("직위 : "),9,0)
        self.layout.addWidget(QLabel("email : "),10,0)
        self.search_box.currentIndexChanged.connect(self.set_user_info)

    def addButtonClicked(self):
        rowPosition = self.add_user_table.rowCount()
        try:
            self.add_user_table.insertRow(rowPosition)
        except:
            self.show_message("재시도")
    def updateButtonClicked(self):
        employee_number = self.employee_number_label.text()
        name = self.name_label.text()
        department= self.department_label.text()
        position = self.position_label.text()
        email = self.email_label.text()
        try:
            result = update.user(
                db= self._db,
                employee_number = employee_number,
                name = name,
                department = department,
                position = position,
                email = email,
                join_user = self.email
            )
            if result ==True:
                self.close()
            else:
                s=QMessageBox.warning(self,'User Update','수정실패',QMessageBox.Yes,QMessageBox.Yes)
        except Exception as e:
            print(e)
        
    def saveButtonClicked(self):
        row_count = self.add_user_table.rowCount()
        col_count = self.add_user_table.columnCount()
        result_list = []
        for i in range(row_count):
            user_info = []
            try:
                for j in range(col_count):
                    user_info.append(self.add_user_table.item(i,j).text())
            except:
                continue
            try:
                result = create.user(
                    db=self._db,
                    name = user_info[0],
                    employee_number = user_info[1],
                    department = user_info[2],
                    position = user_info[3],
                    email = user_info[4],
                    join_user = self.email
                )
                if result != False:
                    result_list.append(result)
                self.close()
            except:
                continue
        self.show_message(result_list)
            
    