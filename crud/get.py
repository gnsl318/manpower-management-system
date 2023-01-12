
from datetime import date
from sqlalchemy import update
from sqlalchemy.orm import Session, load_only
from models.base import *
import datetime
from pytz import timezone


def all_user(
    *,
    db:Session,
):
    user_info=db.query(User).all()
    return user_info

# def get_user(
#     *,
#     db:Session,
# ):
#     user = db.query(User).filter(User.resignation_date == null).all()
#     return user