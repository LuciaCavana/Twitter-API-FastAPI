#Python

#Models
from Models.Tweets import Tweets, ShowTweets, Tweets_class

#FastAPI

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import HTTPException
from fastapi import status
from fastapi import Body, Path

tags_tweets = "Tweets"
tags_users = "Users"

app = FastAPI()

@app.get(path="/", 
    response_model=ShowTweets,
    tags=[tags_tweets],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets"
    )
def home(tweet:Tweets = Body(...)):
    '''
    Home

    This path operation shows all tweets

    Parameter:
    - Request body parameter:
        - **tweet:Tweets** ->  A tweets model with tweet id, user id, username, message and tweet date

    Return ShowTweets model with username, tweets, tweets date
    '''
    #html = """
    #<h1>Twitter API</h1>
    #<div class="col-xs-12">
    #    <div id="respond" class="tweet-respond">
    #        <form action="http://127.0.0.1:8000/" method="post" id "tweetsform" class="" novalidate data-hs-cs-bound="true">
    #            <p>
    #            <br><label for="Tweet">Tweet</label></br>
    #            <textarea required="required" id="Tweet" name="comment" cols="45" rows="8" aria-required="true"></textarea>
    #            </p>
    #        </form>
    #    </div>
    #</div>
    #""" 
    return tweet 
        
@app.post(
    path="/post", 
    status_code=status.HTTP_201_CREATED, 
    tags=[tags_tweets],
    summary="Create tweet",
    response_model= ShowTweets
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

@app.get(
    path="/tweets/{tweet_id}",
    tags=[tags_tweets],
    status_code=status.HTTP_200_OK,
    summary="Show a specific tweet"
    )
def show_tweet(
    tweet_id:int = Path(..., gt=0, title="Tweet id", description="This is a tweet id")
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
    tags=[tags_tweets],
    summary="Delete tweets",
    status_code=status.HTTP_200_OK
)
def delete_tweet(
    Tweet_id:int = Path(...,gt=0,title="Tweet ID",description="enter the id tweet ")
):
    '''
    Tweet Delete

    This path operation an id of a tweet is entered and removed from the database

    parameter:
    - Request path operation:
        - **tweet_id:int** -> id of the tweet you want to delete in the database

    Return menssage successful 
    '''
    if Tweet_id not in Tweets_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="the required tweet id does not exist!"
        )

    return "the tweet was deleted successfully"

@app.post(
    path="/tweets/{tweet_id}/update",
    tags=[tags_tweets],
    summary="Update tweet",
    status_code= status.HTTP_200_OK
)
def update_tweet(
    Tweet_id:int = Path(...,gt=0,title="Tweet ID",description="enter the id tweet ")
):
    '''
    Update tweet

    This path operation an id of a tweet is entered and modify from the database

    parameter:
    -Request path operation:
        -**tweet_id:int** -> id of the tweet you want to update in the database

    Return menssage successful 
    '''
    if Tweet_id not in Tweets_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="the required tweet id does not exist!"
        )
    return "Tweet modify successful"
