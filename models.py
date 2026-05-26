from datetime import datetime
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, Numeric, String
from database import Base

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class BubbleTeaDB(Base):
    __tablename__ = "bubble_teas"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    temperature = Column(String(20), nullable=False)
    price = Column(Numeric(5, 2), nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)