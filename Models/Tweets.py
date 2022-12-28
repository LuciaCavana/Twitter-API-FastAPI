from typing import Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import Field



class Tweets(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ..., 
        min_length=1, 
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    update_at: Optional[datetime] = Field(default=datetime.now())
    id_user: UUID = Field(...)
    class Config:
        schema_extra={
            "example":{
                 "tweet_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                 "content": "Hola, este es mi primer tweet",
                 "created_at": datetime.now(), 
                 "update_at":datetime.now(),
                 "id_user":"3fa85f64-5717-4562-b3fc-2c963f66afa6"
            }
        }
