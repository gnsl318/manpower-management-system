
from datetime import date
from sqlalchemy import update
from sqlalchemy.orm import Session, load_only
from models.base import *
from datetime import datetime
from pytz import timezone
timezone = timezone('Asia/Seoul')
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
        if db.query(User).filter(User.name == name).first()==None:
            new_user = User(
                employee_number = employee_number,
                name=name,
                department_id = db.query(Department).filter(Department.department == department).first().id,
                position_id = db.query(Position).filter(Position.position == position).first().id,
                email =email,
                join_date = timezone.localize(datetime.strptime(f'{employee_number[:4]}-{employee_number[4:6]}-{employee_number[6:8]} 00:00:00', '%Y-%m-%d %H:%M:%S')),#datetime.datetime.now(timezone('Asia/Seoul')),
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
    new_department = Department(
        department=department,
    )
    db.add(new_department)
    db.commit()
    return new_department

def position(
    *,
    db:Session,
    position:str,
):
    new_position = Position(
        position=position,
    )
    db.add(new_position)
    db.commit()
    return new_position