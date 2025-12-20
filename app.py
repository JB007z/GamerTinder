from fastapi import FastAPI,Depends,HTTPException,status
from pydantic import BaseModel
from typing import List,Annotated
from database import engine,SessionLocal,get_db
import models
import schemas
from sqlalchemy.orm import Session
from utils import Hash
app = FastAPI()
models.Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session,Depends(get_db)]

@app.post("/register/",response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate,db:db_dependency):
    user_check  = db.query(models.User).filter(models.User.email==user.email).first()
    if user_check:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already being used")

    db_user = models.User(
        username = user.username,
        email = user.email,
        hashed_password = Hash.bcrypt(user.raw_password),
        bio = user.bio,
        profile_image = user.profile_image
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



@app.post("/login/")