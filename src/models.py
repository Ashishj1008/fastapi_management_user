from pydantic import EmailStr
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date
from .database import Base
from datetime import date


class Record(Base):
    __tablename__ = "user_management_details"

    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(30))
    phone = Column(String(15))
    email = Column(String(50))
    address = Column(String(200))
    dob = Column(String(100))
