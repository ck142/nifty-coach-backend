
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, unique=True, index=True)
    symbol = Column(String)
    side = Column(String)
    qty = Column(Float)
    price = Column(Float)
    timestamp = Column(DateTime)

def init_db():
    Base.metadata.create_all(bind=engine)
