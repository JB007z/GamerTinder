from sqlalchemy.orm import Session
import models
from backend import schemas
from backend.utils import Hash
from fastapi import HTTPException,status,UploadFile

def create_user(db: Session, user:schemas.UserCreate):
    email_check  = db.query(models.User).filter(models.User.email ==user.email).first()
    if email_check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email already being used")
    username_check = db.query(models.User).filter(models.User.username==user.username).first()
    if username_check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Username already being used")
    
    hashed_password = Hash.bcrypt(user.raw_password)

    new_user = models.User(

        username = user.username,
        email = user.email,
        bio = user.bio,
        profile_image= user.profile_image,
        hashed_password=hashed_password
    )

    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user  

def get_user_by_email(db:Session,email:str):
    user = db.query(models.User).filter(models.User.email==email).first()
    return user


def get_user_by_username(db:Session,username:str):
    user = db.query(models.User).filter(models.User.username==username).first()
    return user

def update_user(db:Session,user_id:int, bio:str,profile_image:UploadFile):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None

    if bio:
        db_user.bio = bio
    
    if profile_image:
        os.makedirs("static", exist_ok=True)
        file_path = f"static/{profile_image.filename}"
        with open(file_path, "wb") as f:
            f.write(profile_image.file.read())
        db_user.profile_pic = file_path


   

    db.add(db_user) #add pode tanto criar nova row como dar update em uma
    db.commit()
    db.refresh(db_user)
    return db_user


def remove_user(db:Session, user_id:int):
    deleted_user = db.query(models.User).filter(models.User.id==user_id).first()
    if deleted_user:
        db.delete(deleted_user)
        db.commit()
        return True
    
    return False
