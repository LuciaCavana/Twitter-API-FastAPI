#Python
from typing import List
import json

#Function
import function.Files as af

#Models
from Models.User import UserLogin, UserShow, UserRegister


#FastAPI

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi import Body, Path, Query

tags_tweets = "Tweets"
tags_users = "Users"

app = FastAPI()


#Path Operation

##User

###Register a user

@app.post(
    path="/signup",
    response_model=UserShow, 
    status_code=status.HTTP_201_CREATED,
    summary="Register a user",
    tags=[tags_users]

)
def signup(user:UserRegister = Body(...)):
    '''
    Signup

    This pat operation register a user in the app and database

    Parameters:
    - Request body parameter:
        - ***user:UserLogin* ->  A user model with user id, username, password and email
        
    Returns a jason whit the basic information: 
    - ser_id::UUID
    - first_name: str
    - las_name: str
    - email: Emailstr
    - age: int
    - brith_date: Optional[date]
    '''

    user = user.dict()
    user["user_id"] = str(user["user_id"])
    user["birth_date"] = str(user["birth_date"])
    af.include_json("./json/Users.json", user)
    return user

###Login a user

@app.post(
    path="/login",
    response_model=UserShow,
    summary="Login a user",
    status_code=status.HTTP_200_OK, 
    tags=[tags_users])
def login(
    user_id:int = Query(..., gt=0, title="User id", description="This is a user id",example=1)
):
    '''
    Login

    This pat operation login a user in the app

    Parameters:
    - Request body parameter:
        - ***user:User* ->  A user model with user id, username, password, age, email, first name and lastname
        
    Returns a user model with first name, last name, age, user id, username and email
    '''
    if user_id not in User_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="the required user id does not exist!"
        )
    return {user_id:"Exist!"}

###Show All Users

@app.get(
    path="/users",
    response_model=List[UserShow],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=[tags_users]
)

def show_all_users():
    ''' 
    Show all users


    This path operation shows all users

    Parameter:
    - 

    Return a json  list with all user in the app, with the following keys
    - ser_id::UUID
    - first_name: str
    - las_name: str
    - email: Emailstr
    - age: int
    - brith_date: Optional[date]

    '''
    return af.read_json("./json/Users.json")



###Show a user

@app.get(
    path="/users/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserShow,
    summary="Show a user",
    tags=[tags_users]
)
def show_users(

    user_id:str = Path(..., max_length=36, title="User id", description="This is a user id",example="3fa85f64-5717-4562-b3fc-2c963f66afa6")
):
    '''
    Users
    
    this path operation receives an id of a user, looks it up in the database

    parameters:
    - Request path parameter:
        - **user_id:int** -> referenced user id


    Return User model username, first name, last name, age and email

    '''
    with open("./json/Users.json","r",encoding="utf-8") as file:
        for items in json.loads(file.read()) :
            if user_id in items["user_id"]:
                return items
        
###Delete a user

@app.delete(
    path="/user/{user_id}/delete",
    response_model=List[UserShow],
    tags=[tags_users],
    summary="Delete a user",
    status_code=status.HTTP_200_OK

)
def delete_user(
        user_id:str = Path(..., max_length=36, title="User id", description="This is a user id",example="3fa85f64-5717-4562-b3fc-2c963f66afa6")
):
    '''
    Delete user

    This path operation an id of a user is entered and removed from the database

    parameter:
    -Request path operation:
        -**user_id:int** -> id of the user you want to delete in the database

    Return menssage successful 
    '''
#No funciona 
    with open("./json/Users.json","r+",encoding="utf-8") as file:
    
        result= json.loads(file.read())
        for data  in result :
            if user_id == data["user_id"]:  
                result.remove(data)  
                remplace_json(result,"./json/Users.json")
        return result
    

###Update a user

@app.put(
    path="/tweets/{user_id}/update",
    tags=[tags_users],
    response_model=UserShow,
    status_code=status.HTTP_200_OK,
    summary="Update a user"
)
def update_user(
    user_id:int = Path(..., gt=0, title="User id", description="This is a user id",example=1)
):
    '''
    Update user

    This path operation an id of a user is entered and modify from the database

    parameter:
    -Request path operation:
        -**user_id:int** -> id of the user you want to update in the database

    Return menssage successful 
    '''
    pass