from sqlalchemy import Boolean,Column,ForeignKey,Integer,String,Enum,Table,DateTime,UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

user_games_association = Table(
    'user_games',
    Base.metadata,
    Column('user_id',Integer,ForeignKey('users.id'),primary_key=True),
    Column('game_id',Integer,ForeignKey('games.id'),primary_key=True)
)

class PlatformPreference(str,enum.Enum):
    PLAYSTATION = 'playstation'
    XBOX = 'xbox'
    PC = 'pc'

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,index=True)
    username= Column(String(20),unique=True,index=True)
    email = Column(String,unique=True,index=True)
    hashed_password = Column(String)
    bio = Column(String,nullable=True)
    profile_image = Column(String,nullable=True)
    platform = Column(
        Enum(PlatformPreference, name="platform_enum"), 
        nullable=False
    )
    games = relationship("Game",secondary=user_games_association,back_populates="players")


class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True,index = True)
    name = Column(String,unique=True,index=True)
    genre = Column(String,index=True)
    players = relationship("User",secondary=user_games_association,back_populates="games")


class Like(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True, index=True)
    liker_id = Column(Integer,ForeignKey('users.id'),index=True)
    liked_id = Column(Integer,ForeignKey('users.id'),index=True)
    status = Column(String,index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('liker_id','liked_id',name='unique_like_pair'),

    )

class Match(Base):
    __tablename__ = 'matches'
    id = Column(Integer,primary_key=True,index=True)
    user1_id = Column(Integer,ForeignKey('users.id'),index=True)
    user2_id = Column(Integer,ForeignKey('users.id'),index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    user1 = relationship("User", foreign_keys=[user1_id])
    user2 = relationship("User", foreign_keys=[user2_id])
    