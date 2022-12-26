#Python

#Models
from Models.User import User, UserShow, User_class

#FastAPI

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi import Body, Path

tags_users = "Users"

app = FastAPI()

@app.post(
    path="/signup",
    status_code=status.HTTP_201_CREATED,
    tags=[tags_users],
    summary="Register a user",
    response_model=User 
)
def signup(user:UserLogin = Body(...)):
    '''
    Signup

    This pat operation register a user in the database

    Parameters:
    - Request body parameter:
        - ***user:UserLogin* ->  A user model with user id, username, password, age, email, first name and lastname
        
    Returns a user model with first name, last name, age, user id, username and email
    '''
    return user

@app.post(
    path="/login",
    summary="Login a user",
    status_code=status.HTTP_200_OK, 
    tags=[tags_users],
    response_model= List[User]
    )
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

@app.get(
    path="/users",
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=[tags_users],
    response_model=List[User]
)
def show_all_users():
    ''' 
    Show all users

    This path operation shows all users

    Parameter:
    - Request body parameter:
        - **users:Users** ->  A tweets model with tweet id, user id, username, message and tweet date

    Return User model username, first name, last name, age and email
    '''
    return User_class

@app.get(
    path="/users/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Show a user",
    tags=[tags_users],
    response_model=User
)
def show_users(
    user_id:int = Path(..., gt=0, title="User id", description="This is a user id",example=1)
):
    '''
    Users
    
    this path operation receives an id of a user, looks it up in the database

    parameters:
    - Request path parameter:
        - **user_id:int** -> referenced user id

    Return User model username, first name, last name, age and email
    '''
    if user_id not in User_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="the required user id does not exist!"
        )
    return dict(User_class[user_id])

@app.delete(
    path="/user/{user_id}/delete",
    tags=[tags_users],
    response_model= User,
    summary="Delete a user",
    status_code=status.HTTP_200_OK
)
def delete_user(
    user_id:int = Path(..., gt=0, title="User id", description="This is a user id",example=1)
):
    '''
    Delete user

    This path operation an id of a user is entered and removed from the database

    parameter:
    -Request path operation:
        -**user_id:int** -> id of the user you want to delete in the database

    Return menssage successful 
    '''
    if user_id not in User_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="the required user id does not exist!"
        )
    return "the user was deleted successfully"

@app.put(
    path="/tweets/{user_id}/update",
    tags=[tags_users],
    response_model=User,
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
    if user_id not in User_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="the required user id does not exist!"
        )

    return "the user was modify successfully"