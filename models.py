from sqlalchemy import Boolean,Column,ForeignKey,Integer,String
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,index=True)
    username= Column(String,unique=True,index=True)
    email = Column(String,unique=True,index=True)
    hashed_password = Column(String)
    bio = Column(String,nullable=True)
    profile_image= Column(String,nullable=True)
    


