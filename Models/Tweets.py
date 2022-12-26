from typing import Optional
from datetime import datetime
from uuid import UUID

from .User import UserShow

from pydantic import BaseModel
from pydantic import Field



Tweets_class = {
    1:{
        "user_id": 1,
        "username":"Lucia",
        "contet": "Hola, soy Lucia y este es mi primer Tweet",
        "Tweet_date":"26-12-2022"
    },
    2:{
        "user_id": 2,
        "username":"Martina",
        "contet": "Hola, soy Martina y este es mi primer Tweet",
        "Tweet_date":"26-12-2022"
    },
    3:{
        "user_id": 3,
        "username":"Roberto",
        "contet": "Hola, soy Roberto y este es mi primer Tweet",
        "Tweet_date":"26-12-2022"
    },
}


class Tweets(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ..., 
        min_length=1, 
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    update_at: Optional[datetime] = Field(default=None)
    by: UserShow = Field(...)
