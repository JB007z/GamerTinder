from fastapi import FastAPI,Depends,HTTPException,status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List,Annotated
from database import engine,SessionLocal,get_db
import models
from backend import schemas,crud
from backend.utils import Hash
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



