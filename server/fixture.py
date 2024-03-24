from models import Base, Student
from database import engine, SessionLocal
from datetime import datetime


def fixture():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    session = SessionLocal()
    
    when = datetime.strptime("2021-02-18 16:39:00 UTC", "%Y-%m-%d %H:%M:%S UTC")
    s1 = Student(first_name="Jim", last_name="Hawkins", email="test1@ucla.edu")
    s2 = Student(first_name="Sally", last_name="Ride", email="test2@ucla.edu")
    when = datetime.strptime("2023-01-31 22:20:37 UTC", "%Y-%m-%d %H:%M:%S UTC")
    s3 = Student(first_name="Jason", last_name="Bourne", email="test3@ucla.edu")
    
    session.add_all([s1, s2, s3])
    session.commit()
    session.close()
    
if __name__ == "__main__":
    fixture()