from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from typing import List

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    # check_in_time = Column(DateTime, nullable=True)
    # check_in_time = Column(DateTime, nullable=False, default=datetime.now())
    check_ins = relationship("CheckIn", back_populates="student", cascade="all, delete")
    
    def __repr__(self):
        return f"<Student {self.id}: {self.first_name} {self.last_name} {self.check_in_time}"
    
class CheckIn(Base):
    __tablename__ = "check_ins"
    id = Column(Integer, primary_key=True)
    major = Column(String, nullable=False)
    email = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    check_in_time = Column(DateTime, nullable=False)
    student_id = Column(ForeignKey("students.id", ondelete="CASCADE"))
    student = relationship("Student", back_populates="check_ins")

    

    
    
