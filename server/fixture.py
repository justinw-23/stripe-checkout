from models import Base, Book, Customer
from database import engine, SessionLocal
from datetime import datetime


def fixture():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    session = SessionLocal()
    
    # c1 = Customer(name="Anne Smith")
    # c2 = Customer(name="John Doe")
    # c3 = Customer(name="Jason Bourne")
    
    b1 = Book(title="National Parks", stock=100, sold=0)
    
    # session.add_all([c1, c2, c3, b1])
    session.add(b1)
    session.commit()
    session.close()
    
if __name__ == "__main__":
    fixture()