#Python
from typing import List
import json

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
    return Tweets_class 

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
    tweet_id:int = Path(..., gt=0, title="Tweet id", description="This is a tweet id",example=1)
):
    '''
    Show tweet

    this path operation receives an id of a tweet, looks it up in the database

    parameters:
    - Request path parameter:
        - **tweet_id:int** -> referenced tweet id

    Return the username, the tweet, and the date of the tweet
    '''
    if tweet_id not in Tweets_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="the required tweet id does not exist!"
        )
    return dict(Tweets_class[tweet_id])

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

