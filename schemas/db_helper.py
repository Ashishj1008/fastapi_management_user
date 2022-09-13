from typing import Optional

from pydantic import BaseModel, validator, ValidationError, EmailStr
from datetime import date


class UserDetail(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: EmailStr
    address: str
    dob: date

    class Config:
        orm_mode = True

    @validator('phone')
    def check(cls, v):
        if len(v) != 10:
            raise ValidationError("please enter the correct phone number")
        return v





class UpdateDetails(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]
    address: Optional[str]
    dob: Optional[date]

    class Config:
        orm_mode = True

    @validator('phone')
    def check(cls, v):
        if len(v) != 10:
            raise ValidationError("please enter the correct phone number")
        return v













