from uuid import UUID
from typing import Optional
from datetime import date

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    user_email:EmailStr=Field(...,title="User email", description="This is the user email")


class UserLogin(UserBase):
    username:str=Field(..., max_length=20, min_length=1, title="Username", description="This is the Username")
    password: str = Field(..., min_length=8, max_length=64)

    class Config:
        schema_extra={
            "example":{
                "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                 "username": "LucyDanny",
                 "password": "admin123",
                 "user_email":"lucia@example.com"
                }
        }

class UserShow(UserBase):
    first_name:str =Field(..., max_length=20, min_length=1, title="First Name", description="This is the user first name")
    last_name:str=Field(..., max_length=20, min_length=1, title="Last name", description="This is the user last name")
    user_age:int=Field(..., gt=17, lt=115,title="User age", description="This is the user age")
    birth_date: Optional[date] = Field(default=None)

class UserRegister(UserShow):

    username:str=Field(..., max_length=20, min_length=1, title="Username", description="This is the Username")
    password: str = Field(..., min_length=8, max_length=64)

    class Config:
        schema_extra={
            "example":{
                 "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                 "username": "LucyDany",
                 "password": "admin123", 
                 "user_email":"lucia@example.com",
                 "first_name":"Lucia",
                 "last_name":"Cavana",
                 "user_age":22,
                 "birth_date":"2000-12-22"
                }
        }
