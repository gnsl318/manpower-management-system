import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QDate,Qt
from db import session
from crud import create,get


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

    
    @staticmethod
    def show_message(message):
        msg = QMessageBox()
        msg.setText(message)
        msg.exec_()

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
            except:
                continue
        self.show_message(result_list)
            
        # try:
        #     create_user(
        #         db=self._db,
        #         employee_number = self.user_employee_number,
        #         name = self.user_name,
        #         email = self.user_email
        #     )
        #     self.close()
        # except:
        #     self.show_message("재시도")        