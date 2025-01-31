from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DATABASE_URL = "sqlite:///./chain_store/database.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Staff(Base):
    __tablename__ = 'Staff'
    
    employee_code = Column(Integer, primary_key=True)
    name_and_surname = Column(String(255))
    national_code = Column(String(255))
    date_of_entry = Column(Date)
    date_of_birth = Column(Date)

class Customers(Base):
    __tablename__ = 'Customers'
    
    customer_id = Column(Integer, primary_key=True)
    name_and_surname = Column(String(255))

class Products(Base):
    __tablename__ = 'Products'
    
    product_code = Column(Integer, primary_key=True)
    product_name = Column(String(255))
    price = Column(Numeric)

class Cart(Base):
    __tablename__ = 'Cart'
    
    cart_id = Column(Integer, primary_key=True)
    product_code = Column(Integer, ForeignKey('Products.product_code'))
    quantity = Column(Integer, default=1)
    
    product = relationship("Products")

class Branches(Base):
    __tablename__ = 'Branches'
    
    branch_id = Column(Integer, primary_key=True)
    address = Column(String(255))

class Payment(Base):
    __tablename__ = 'Payment'
    
    payment_id = Column(Integer, primary_key=True)
    amount = Column(Numeric)
    customer_id = Column(Integer, ForeignKey('Customers.customer_id'))
    branch_id = Column(Integer, ForeignKey('Branches.branch_id'))
