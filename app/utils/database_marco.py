from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



SQLALCHEMY_DATABASE_URL="postgresql://marco_admin_user:fuB4WQqK@marco-dev.cluster-ceig96elcanm.us-east-1.rds.amazonaws.com:5432/marco"
engine = create_engine(SQLALCHEMY_DATABASE_URL) # engine to talk with DB

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine) # responsible for talking with the databases

Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

