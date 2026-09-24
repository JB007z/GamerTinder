import os
import models, database
from backend import schemas
from datetime import datetime,timedelta
from typing import Optional
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACESS_TOKEN_EXPIRES = 60*24

pwd_context = CryptContext(schemes=["argon2"],deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")




def create_acess_token(data:dict, expires_delta: Optional[timedelta]=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow()+expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token:str = Depends(oauth2_scheme),db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:

        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email:str = payload.get("sub")
        if email is None:
            print("no email")
            raise credentials_exception
        token_data =schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception 

    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        print("no user")
        raise credentials_exception

    return user


