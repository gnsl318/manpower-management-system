
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
        user_info = db.query(User).filter(User.employee_number == employee_number).first()
        user_dic=user_info.__dict__
        for key,value in {"name":name,"email":email,"department_id":department,"position_id":position}.items():
            if key =="department_id":
                value=db.query(Department).filter(Department.department==department).first().id
            if key =="position_id":
                value=db.query(Position).filter(Position.position==position).first().id
            if user_dic[key] != value:
                raw = f"{key}-{user_dic[key]}"
                change = f"{key}-{value}"
                if key =="name":
                    user_info.name=value
                elif key =="email":
                    user_info.email=value
                elif key =="department_id":
                    user_info.department_id=value
                elif key =="position_id":
                    user_info.position_id=value

                user_log = User_Log(
                    user_id=user_info.id,
                    raw = raw,
                    change = change,
                    change_date = datetime.now(timezone('Asia/Seoul')),
                    change_user_id = db.query(User).filter(User.email == join_user).first().id
                )
                db.add(user_log)
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False

