
from datetime import date
from sqlalchemy import and_
from sqlalchemy.orm import Session, load_only
from models.base import *
from datetime import datetime
from pytz import timezone
import json

def user(
    *,
    db : Session,
    employee_number:str,
    name:str,
    email:str,
    department:str,
    position:str,
    join_user:str,
):
    try:
        raw={}
        change={}

        user_info = db.query(User).filter(User.employee_number == employee_number).first()

        if user_info.name != name:
            raw['이름']=user_info.name
            change['이름']=name
            user_info.name=name
        elif user_info.email!=email:
            raw['email'] = user_info.email
            change['email']=email
            user_info.email=email
        elif user_info.department.department!=department:
            raw['부서'] = user_info.department.department
            change['부서']=department
            user_info.department_id = db.query(Department).filter(Department.department==department).first().id
        elif user_info.position.position !=position:
            raw['직위'] = user_info.position.position
            change['직위']=position
            user_info.position_id = db.query(Position).filter(Position.position==position).first().id
        user_log = User_Log(
            user_id=user_info.id,
            raw = json.dumps(raw,ensure_ascii=False),
            change = json.dumps(change,ensure_ascii=False),
            change_date = datetime.now(timezone('Asia/Seoul')),
            change_user_id = db.query(User).filter(User.email == join_user).first().id
        )
        db.add(user_log)
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False

def user_resignation(
    db:Session,
    name:str,
    edit_user_email:str
):
    try:
        user_info = db.query(User).filter(and_(User.name == name,User.resignation_date==None)).first()
        user_info.resignation_date = datetime.now(timezone('Asia/Seoul'))
        user_log = User_Log(
            user_id=user_info.id,
            raw = "",
            change = "퇴사",
            change_date = datetime.now(timezone('Asia/Seoul')),
            change_user_id = db.query(User).filter(User.email == edit_user_email).first().id
        )
        db.add(user_log)
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False
    

def department(
    db : Session,
    raw_department : str,
    department : str
):
    department_info = db.query(Department).filter(Department.department==raw_department).first()
    if department_info==None:
        return False
    else:
       department_info.department = department
    db.commit()
    return True
    
def position(
    db : Session,
    raw_position : str,
    position : str
):
    position_info = db.query(Position).filter(Position.position==raw_position).first()
    if position_info==None:
        return False
    else:
       position_info.position = position
    db.commit()
    return True