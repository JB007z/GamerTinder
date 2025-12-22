from sqlalchemy.orm import Session
import models
from backend import schemas
from backend.utils import Hash

def create_user(db: Session, user:schemas.UserCreate):
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

def update_user(db:Session,user_id:int, user_update:schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None

    update_data = user_update.dict(exclude_unset=True)
    for key,value in update_data.items():
        setattr(db_user,key,value)

    #verificação dinamica não leva em conta update de senha e username
    #esses updates acarretariam mais mudanças (hashed password e token)


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
