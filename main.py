#Python
from typing import List
#Function
import function.Files as af

#Models
from Models.Tweets import Tweets
from Models.User import UserShow, UserRegister

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

    Return Tweets model with:
    -**tweet_id:UUID**
    -**content: str**
    -**created_at:datetime**
    -**update_at:datetime**
    -**id_user:UUID**
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

    Return tweets model with:
    -**tweet_id:UUID**
    -**content: str**
    -**created_at:datetime**
    -**update_at:datetime**
    -**id_user:UUID**
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
    tweet_id:str = Path(..., max_length=36, min_length=36, title="Tweet id", description="This is a tweet id",example="3fa85f64-5717-4562-b3fc-2c963f66afa6")
):
    '''
    Show tweet

    this path operation receives an id of a tweet, looks it up in the database

    parameters:
    - Request path parameter:
        - **tweet_id:str** -> referenced tweet id

    Return tweet models with:
    -**tweet_id:UUID**
    -**content: str**
    -**created_at:datetime**
    -**update_at:datetime**
    -**id_user:UUID**
    '''
    result = af.return_entidad_expesifiqued("./json/Tweets.json", tweet_id,"tweet_id")
    return result

@app.delete(
    path="/tweets/{tweet_id}/delete",
    status_code=status.HTTP_200_OK,
    summary="Delete tweets",
    tags=[tags_tweets]
)
def delete_tweet(
    tweet_id:str = Path(...,max_length=36,min_length=36,title="Tweet ID",description="enter the id tweet ",example=1)
):
    '''
    Tweet Delete

    This path operation an id of a tweet is entered and removed from the database

    parameter:
    - Request path operation:
        - **tweet_id:str** -> id of the tweet you want to delete in the database

    Return menssage successful or not
    '''

    return af.delete("./json/Tweets.json",tweet_id, "tweet_id","Tweet deleted successfully","Non-existent tweet id!")
    
###Update a tweet

@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweets,
    summary="Update tweet",
    status_code= status.HTTP_200_OK,
    tags=[tags_tweets]
)
def update_tweet(
    tweet_id:str = Path(...,max_length=36,min_length=36,title="Tweet ID",description="enter the id tweet ",example=1),
    tweet:Tweets = Body(...)
):
    '''
    Update tweet

    This path operation an id of a tweet is entered and modify from the database
    -**content:str**
    -**update_at:datetime**

    parameter:
    -Request path operation:
        -**tweet_id:str** -> id of the tweet you want to update in the database

    Return menssage successful or not
    '''

    item = af.return_entidad_expesifiqued("./json/Tweets.json",tweet_id,"tweet_id")
    tweet = tweet.dict()
    tweet["tweet_id"] = tweet_id
    tweet["id_user"] = str(item["id_user"])
    tweet["created_at"] = str(item["created_at"])
    tweet["update_at"] = str(tweet["update_at"])
    
    tweet_update, term = af.update_json("./json/Tweets.json", tweet, (af.read_json("./json/Tweets.json")),tweet_id,"tweet_id")
    if term == False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Non-existent user id!"
        )
    return tweet_update


##User

###Register a user

@app.post(
    path="/signup",
    #response_model=UserShow, 
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

    Users = af.read_json("./json/Users.json") #return dictionary Users
    for user in Users:
       if user["username"] == username and user["password"] == password:
            return "Login exited is user : " + user["username"]
    raise HTTPException(
       status_code=status.HTTP_404_NOT_FOUND,
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
        user_id:str = Path(..., max_length=36, min_length=36,title="User id", description="This is a user id",example="3fa85f64-5717-4562-b3fc-2c963f66afa6")
):
    '''
    Delete user

    This path operation an id of a user is entered and removed from the database

    parameter:
    -Request path operation:
        -**user_id:str** -> id of the user you want to delete in the database

    Return menssage successful or not
    '''

    return af.delete("./json/Users.json",user_id, "user_id","User deleted successfully","Non-existent user id!")

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
    '''
    User tweet

    This path operation an id of a tweet is entered and modify from the database
    -**first_name:str**
    -**last_name:str**
    -**user_age:int**
    -**birth_date:date**

    parameter:
    -Request path operation:
        -**tweet_id:str** -> id of the tweet you want to update in the database

    Return menssage successful or not
    '''
    user_id = str(user_id)
    user = user.dict()
    user["user_id"] = user_id
    user["birth_date"] = str(user["birth_date"])
    
    user, term = af.update_json("./json/Users.json", user, (af.read_json("./json/Users.json")),user_id,"user_id")
    if term == False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Non-existent user id!"
        )
    return user
        