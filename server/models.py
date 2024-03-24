from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from typing import List

Base = declarative_base()

class Book(Base):
    __tablename__= "books"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    stock = Column(Integer, nullable=False)
    sold = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Book {self.id}: {self.title}, {self.sold} sold, {self.stock} in stock."
    
class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    orders = relationship("Order", back_populates="customer", cascade="all, delete")
    
    def __repr__(self):
        return f"<Customer {self.id}: {self.name}"

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    book_id = Column(ForeignKey("books.id"))
    customer_id = Column(ForeignKey("customers.id"))
    customer = relationship("Customer", back_populates="orders")
    quantity = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Order {self.id}: customer {self.customer_id}, book {self.book_id}, purchased {self.quantity}."


    

    
    
