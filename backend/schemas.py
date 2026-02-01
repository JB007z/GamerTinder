from pydantic import BaseModel,EmailStr,field_validator
from typing import List,Optional
from datetime import datetime
from enum import Enum


class UserBase(BaseModel):
    username:str
    email:EmailStr
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    @field_validator('username')
    @classmethod
    def username_restraints(cls,v:str):
        if not v.isalnum:
            raise ValueError("Username must only contain numbers and letters!")
        if (len(v)<4):
            raise ValueError("Username must have at least 4 characters!")
        if (len(v)>20):
            raise ValueError("Username must have at most 20 characters!")
        return v
    


class UserCreate(UserBase):
    raw_password: str  
    @field_validator('raw_password')
    @classmethod
    def password_restraints(cls,v:str):
        if v.isalnum:
            raise ValueError("Password must contain at least one special symbol")
        if (len(v)<4):
            raise ValueError("Password must have at least 4 characters!")
        if (len(v)>20):
            raise ValueError("Password must have at most 20 characters!")

class UserUpdate(BaseModel):
    email:Optional[EmailStr] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None

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
    email:str|None= None