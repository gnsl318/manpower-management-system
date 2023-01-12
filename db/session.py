
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

load_dotenv(verbose=True)
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')

# window exe 로만들땐 DB_URL을 직접 적어서 넣어줘야함
engine = create_engine(SQLALCHEMY_DATABASE_URI,echo=False,pool_size=500,pool_recycle=500,pool_pre_ping=True,max_overflow=20,pool_timeout=500,client_encoding='utf8')
# timeout=600,pool_recycle=500)#,
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
#session = SessionLocal()


def get_db():
        db = SessionLocal()
        try:
                yield db
        except:
                db.rollback()
                raise
        finally:
                db.close()