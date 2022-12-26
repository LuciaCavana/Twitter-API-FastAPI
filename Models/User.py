from uuid import UUID
from typing import Optional
from datetime import date

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


User_class = {
    1:{
        "username":"Lucia",
        "first_name": "Lucia",
        "last_name":"Cavana",
        "user_email":"lucia@example.com",
        "age": 22
    },
    2:{
        "username":"Martina",
        "first_name": "Martina",
        "last_name":"Garcia",
        "user_email":"martina@example.com",
        "age": 30
    },
    3:{
        "username":"Roberto",
        "first_name": "Roberto",
        "last_name":"Diaz",
        "user_email":"roberto@example.com",
        "age": 18
    },
}

class UserBase(BaseModel):
    user_id: Optional[UUID] = Field(default=None)
    user_email:EmailStr=Field(...,title="User email", description="This is the user email")


class UserLogin(UserBase):
    username:str=Field(..., max_length=20, min_length=1, title="Username", description="This is the Username")
    password: str = Field(..., min_length=8, max_length=64)

    class Config:
        schema_extra={
            "example":{
                 "user_id": 1,
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
                 "user_id": 1,
                 "username": "LucyDanny",
                 "password": "admin123",
                 "user_email":"lucia@example.com",
                 "firs_name":"Lucia",
                 "last_name":"Cavana",
                 "age":22,
                 "brith_date":"22-12-2000",
                }
        }