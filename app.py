from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List,Annotated
from database import engine,SessionLocal,get_db
from backend import schemas,crud,auth
from backend.utils import Hash
from backend.auth import get_current_user
from datetime import timedelta,datetime,timezone
import models
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # só para DEV
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session,Depends(get_db)]

@app.get("/")
def default_response():
    return {"message":"Server is running lil bro"}

@app.post("/register/",response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate,db:db_dependency):
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

@app.get("/profiles",response_model=List[schemas.UserResponse])
def get_profiles(
    db:db_dependency,
    current_user:models.User = Depends(get_current_user),
    limit:int =20

):
    swiped_users = (
        db.query(models.Like.liked_id).filter(models.Like.liker_id==current_user.id)
    ).subquery()

    profiles = db.query(models.User).filter(models.User.id!=current_user.id).filter(~models.User.id.in_(swiped_users)).limit(limit=limit)

    return profiles


@app.post("/swipe")
def swipe_profile(
    like:schemas.LikeCreate,
    db:db_dependency,
    current_user:models.User = Depends(get_current_user)
):
    exists = db.query(models.Like).filter((models.Like.liker_id == current_user.id) & (models.Like.liked_id==like.liked_id)).first()
    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already liked this user"
        )
    new_like = models.Like(
        liker_id =current_user.id ,
        liked_id = like.liked_id,
        status = like.status, 
        
    )
    db.add(new_like)
    db.commit()
    db.refresh(new_like)


    match = db.query(models.Like).filter((models.Like.liker_id==like.liked_id)&(models.Like.liked_id==current_user.id)).first()
    if match:
        new_match = models.Match(
            user1_id = current_user.id,
            user2_id = like.liked_id,
         
        )
        db.add(new_match)
        db.commit()
        db.refresh(new_match)


    return new_like



@app.get("/matches")
def get_matches(
    db:db_dependency,
    user:models.User=Depends(get_current_user)
    ):

    matches = db.query(models.Match).filter((models.Match.user1_id==user.id)|(models.Match.user2_id==user.id)).order_by(models.Match.timestamp.desc()).all()
    return matches