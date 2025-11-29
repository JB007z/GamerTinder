from pydantic import BaseModel,EmailStr
from typing import List,Optional
from datetime import datetime
from enum import Enum


class UserBase(BaseModel):
    username:str
    email:EmailStr
    bio: Optional[str] = None
    profile_image: Optional[str] = None


class UserCreate(UserBase):
    raw_password: str


class UserResponse(UserBase):
    id:int

    class Config:
        from_attributes = True

class GameBase(BaseModel):
    name:str
    genre:str
    platform:str


class GameCreate(GameBase):
    pass


class GameResponse(GameBase):
    id:int
    class Config:
        from_attributes = True


class LikeStatus(str,Enum):
    like = "like"
    dislike  = "dislike"
    superlike = "superlike"

class LikeBase(BaseModel):
    status:LikeStatus = LikeStatus.like

class LikeCreate(LikeBase):
    liked_id :int

class LikeResponse(LikeBase):
    id:int
    liker_id:int
    liked_id:int
    timestamp:datetime
    class Config:
        from_attributes = True


class MatchBase(BaseModel):
    pass

class MatchCreate(MatchBase):
    user1_id : int
    user2_id:int

class MatchResponse(BaseModel):
    id:int
    user1:UserResponse
    user2:UserResponse



class Token(BaseModel):
    access_token:str
    token_type:str


class TokenData(BaseModel):
    username:str|None= None