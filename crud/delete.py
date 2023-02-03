from datetime import date

from sqlalchemy.orm import Session, load_only
from models.base import *
from datetime import datetime
from pytz import timezone



def department(
    db : Session,
    department : str
):
    try:
        department_check = db.query(User).filter(User.department.has(department=department)).first()
        if department_check==None:
            db.query(Department).filter(Department.department==department).delete()
            db.commit()
            return 0
        else:
            return 2
    except:
        return 1

def position(
    db : Session,
    position : str
):
    try:
        position_check = db.query(User).filter(User.position.has(position=position)).all()
        if position_check==None:
            db.query(Position).filter(Position.position==position).delete()
            db.commit()
            return 0
        else:
            return 2
    except:
        return 1