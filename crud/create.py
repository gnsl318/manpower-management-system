
from datetime import date

from sqlalchemy.orm import Session, load_only
from models.base import *
from datetime import datetime
from pytz import timezone

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
        if db.query(User).filter(User.email == email).first()==None:
            new_user = User(
                employee_number = employee_number,
                name=name,
                department_id = db.query(Department).filter(Department.department == department).first().id,
                position_id = db.query(Position).filter(Position.position == position).first().id,
                email =email,
                join_date = datetime.now(timezone('Asia/Seoul')),
                join_user_id = db.query(User).filter(User.email == join_user).first().id
            )
            db.add(new_user)
            db.commit()
            return name
    except:
        return False

def department(
    *,
    db:Session,
    department:str,
):  
    try:
        new_department = Department(
            department=department,
        )
        db.add(new_department)
        db.commit()
        return new_department
    except Exception as e:
        print(e)
        return False
    

def position(
    *,
    db:Session,
    position:str,
):
    try:
        new_position = Position(
            position=position,
        )
        db.add(new_position)
        db.commit()
        return new_position
    except Exception as e:
        print(e)
        return False