from fastapi import FastAPI
from pydantic import BaseModel
from typing import List,Annotated
from database import engine,SessionLocal

app = FastAPI()



