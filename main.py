#Python
from typing import List, Optional
import json
from datetime import date

#Function
import function.Files as af

#Models
from Models.Tweets import Tweets, Tweets_class
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

##Tweets

###Show all Tweets

@app.get(path="/", 
    response_model=List[Tweets],
    tags=[tags_tweets],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets"
    )
def home():

    '''
    Home

    This path operation shows all tweets

    Parameter:
    - Request body parameter:
        - **tweet:Tweets** ->  A tweets model with tweet id, user id, username, message and tweet date

    Return ShowTweets model with username, tweets, tweets date
    '''
    return af.read_json("./json/Tweets.json")

###Post a tweet


@app.post(
    path="/post", 
    response_model= Tweets,
    status_code=status.HTTP_201_CREATED, 
    summary="Post tweet",
    tags=[tags_tweets]
    )
def post(tweets:Tweets = Body(...)):
    '''
    post
    
    this path operation create a tweet 

    Parameter:
    - Request body parameter:
        - **tweet:Tweets** -> A tweets model with tweet id, user id, username, message and tweet date

    Return ShowTweets model with username, tweets, tweets date
    '''
    tweets =tweets.dict()
    tweets["tweet_id"] = str(tweets["tweet_id"])
    tweets["created_at"] = str(tweets["created_at"])
    tweets["update_at"] = str(tweets["update_at"])
    tweets["id_user"] = str(tweets["id_user"])

    af.include_json("./json/Tweets.json",tweets)
    return tweets


###Show a tweet

@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweets,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=[tags_tweets]

    )
def show_tweet(
    tweet_id:str = Path(..., max_length=36, min_length=36, title="Tweet id", description="This is a tweet id",example=1)
):
    '''
    Show tweet

    this path operation receives an id of a tweet, looks it up in the database

    parameters:
    - Request path parameter:
        - **tweet_id:int** -> referenced tweet id

    Return the username, the tweet, and the date of the tweet
    '''
    result = af.return_entidad_expesifiqued("./json/Tweets.json", tweet_id,"tweet_id")
    return result

@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweets,
    status_code=status.HTTP_200_OK,
    summary="Delete tweets",
    tags=[tags_tweets]
)
def delete_tweet(
    tweet_id:int = Path(...,gt=0,title="Tweet ID",description="enter the id tweet ",example=1)
):
    '''
    Tweet Delete

    This path operation an id of a tweet is entered and removed from the database

    parameter:
    - Request path operation:
        - **tweet_id:int** -> id of the tweet you want to delete in the database

    Return menssage successful 
    '''
    if tweet_id not in Tweets_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="the required tweet id does not exist!"
        )

    return "the tweet was deleted successfully"

###Update a tweet

@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweets,
    summary="Update tweet",
    status_code= status.HTTP_200_OK,
    tags=[tags_tweets]
)
def update_tweet(
    tweet_id:int = Path(...,gt=0,title="Tweet ID",description="enter the id tweet ",example=1)
):
    '''
    Update tweet

    This path operation an id of a tweet is entered and modify from the database

    parameter:
    -Request path operation:
        -**tweet_id:int** -> id of the tweet you want to update in the database

    Return menssage successful 
    '''
    if tweet_id not in Tweets_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="the required tweet id does not exist!"
        )
    return "Tweet modify successful"


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
    #response_model=UserShow,
    summary="Login a user",
    status_code=status.HTTP_200_OK, 
    tags=[tags_users])
def login(
    username:str = Query(default="LucyDany", max_length=20, min_length=1, title="Username", description="This is the Username"),
    password:str = Query(default="admin123", min_length=8, max_length=64)
):
    '''
    Login

    This pat operation login a user in the app

    Parameters:
    - Request body parameter:
        - ***user:User* ->  A user model with user id, username, password, age, email, first name and lastname
        
    Returns a user model with first name, last name, age, user id, username and email
    '''
    users_dict = af.read_json("./json/Users.json") #return dictionary Users
    for user in users_dict:
       if user["username"] == username and user["password"] == password:
            return "Login exited is user : " + user["username"]
    raise HTTPException(
       status_code=status.HTTP_404_NOT_FOUNDs,
       detail= "Password or username is incorrect"
    )  

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

    return af.return_entidad_expesifiqued("./json/Users.json",user_id, "user_id")

        
###Delete a user

@app.delete(
    path="/user/{user_id}/delete",
    #response_model=List[UserShow],
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

    Return menssage successful or not
    '''
    path = "./json/Users.json"
    try:
        results = af.read_json(path)
        user = af.return_entidad_expesifiqued(path, user_id, "user_id")
        results.remove(user)
        af.remplace_json(path,results)
        return "User deleted successfully"
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Non-existent user id!"
        ) 
    
    

###Update a user

@app.put(
    path="/user/{user_id}/update",
    tags=[tags_users],
    response_model=UserShow,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
)
def update_user(
        user_id:str = Path(..., max_length=36 , title="User id", description="This is a user id",example=1),
        user:UserShow = Body(...)
    ):

    user_id = str(user_id)
    user = user.dict()
    user["user_id"] = str(user["user_id"])
    user["birth_date"] = str(user["birth_date"])
    
    user, term = af.update_json("./json/Users.json", user, (af.read_json("./json/Users.json")),user_id)
    if term == False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Non-existent user id!"
        )
    return user
        