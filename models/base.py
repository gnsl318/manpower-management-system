from sqlalchemy import Column, Integer, String, ForeignKey, Time, func, Boolean, DateTime,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from db.session import Base,engine

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True, autoincrement=True, index=True)
  employee_number = Column(String(3000),unique=True)
  name = Column(String(3000))
  department_id = Column(Integer,ForeignKey("department.id"))
  department = relationship("Department")
  position_id = Column(Integer,ForeignKey("position.id"))
  position = relationship("Position")
  email = Column(String(3000))
  join_date = Column(DateTime(timezone=True), nullable=False)
  resignation_date = Column(DateTime(timezone=True))
  join_user_id = Column(Integer,ForeignKey("users.id"))
  join_user = relationship("User",foreign_keys=[join_user_id])
  etc = Column(String(3000))

class Department(Base):
  __tablename__ = 'department'
  id = Column(Integer, primary_key=True,autoincrement=True,index=True)
  department = Column(String(3000))

class Position(Base):
  __tablename__ = "position"
  id = Column(Integer, primary_key=True,autoincrement=True,index=True)
  position = Column(String(3000))

class User_Log(Base):
  __tablename__ = "user_log"
  id = Column(Integer, primary_key = True, autoincrement=True,index=True)
  user_id = Column(Integer,ForeignKey("users.id"))
  user =  relationship("User",foreign_keys=[user_id])
  raw = Column(String(3000))
  change = Column(String(3000))
  change_date = Column(DateTime(timezone=True))
  change_user_id = Column(Integer,ForeignKey("users.id"))
  change_user = relationship("User",foreign_keys=[change_user_id])


class Post_Log(Base):
  __tablename__ = "post_log"
  id = Column(Integer, primary_key = True, autoincrement=True,index=True)
  user_id = Column(Integer,ForeignKey("users.id"))
  user =  relationship("User",foreign_keys=[user_id])
  post_date = Column(DateTime(timezone=True))
  result = Column(String(3000))
  post_user_id = Column(Integer,ForeignKey("users.id"))
  post_user = relationship("User",foreign_keys=[post_user_id])


#Test_log.__table__.create(bind=engine)



