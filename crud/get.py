
from datetime import date
from sqlalchemy import and_
from sqlalchemy.orm import Session, load_only
from models.base import *
import datetime
from pytz import timezone


def user(
    *,
    db:Session,
):
    user_info=db.query(User).order_by(User.employee_number).all()
    return user_info

def user_true(
    *,
    db:Session,
):
    user_info=db.query(User).filter(User.resignation_date==None).order_by(User.employee_number).all()
    return user_info
def department(
    *,
    db:Session,
):
    department_info=db.query(Department).all()
    return department_info

def position(
    *,
    db:Session,
):
    position_info=db.query(Position).all()
    return position_info

def user_department(
    *,
    db:Session,
    department:str,
):
    user_info = db.query(User).filter(User.department.has(department=department)).all()
    return user_info

def user_position(
    *,
    db:Session,
    position:str,
):
    user_info = db.query(User).filter(User.position.has(position=position)).all()
    return user_info

def user_dep_pos(
    *,
    db:Session,
    department:str,
    position:str,
):
    user_info = db.query(User).filter(and_(User.department.has(department=department),User.position.has(position=position))).all()
    return user_info


def user_log(
    *,
    db:Session,
):
    user_logs = db.query(User_Log).all()
    return user_logs
    
def post_log(
    *,
    db:Session,
):
    post_logs = db.query(Post_Log).all()
    return post_logs