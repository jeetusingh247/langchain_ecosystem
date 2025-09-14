from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

engine = create_engine('sqlite:///./test.db', connect_args={"check_same_thread": False})
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    orders = relationship('Order', back_populates='user')

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product = Column(String)
    amount = Column(Integer)
    order_date = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship('User', back_populates='orders')

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Add dummy users
users = [
    User(name='Alice', email='alice@example.com'),
    User(name='Bob', email='bob@example.com'),
    User(name='Charlie', email='charlie@example.com'),
]
session.add_all(users)
session.commit()

# Add dummy orders
orders = [
    Order(user_id=1, product='Book', amount=2),
    Order(user_id=1, product='Pen', amount=5),
    Order(user_id=2, product='Notebook', amount=1),
    Order(user_id=3, product='Pencil', amount=10),
]
session.add_all(orders)
session.commit()
session.close()
