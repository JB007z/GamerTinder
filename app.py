from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List,Annotated
from database import engine,SessionLocal,get_db
from backend import schemas,crud,auth
from backend.utils import Hash
from datetime import timedelta
import models
app = FastAPI()
models.Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session,Depends(get_db)]

@app.get("/")
def default_response():
    return {"message":"Server is running lil bro"}

@app.post("/register/",response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate,db:db_dependency):
    user_check  = crud.get_user_by_email(db,user.email)
    if user_check:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already being used")

    return crud.create_user(db=db,user=user)

@app.post("/login")
def login_user(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    #we use form_data.username because its the default for the form_data object
    #even if its the email and not the username (its just the name of the field)
    user = crud.get_user_by_email(db,email=form_data.username) 
    if not user or not Hash.verify(form_data.password,user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expires = timedelta(minutes=auth.ACESS_TOKEN_EXPIRES)
    access_token = auth.create_acess_token(
        data={"sub":user.email},
        expires_delta= access_token_expires
    )
    return {"access_token":access_token,"token_type":"bearer"}



