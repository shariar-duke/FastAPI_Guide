from fastapi import FastAPI, Depends , Response,status , HTTPException
from . import models, schema , utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import List
from dotenv import load_dotenv
import os

from .routers import post, user , auth

load_dotenv()

# Create tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()

print("Shariar")
print(int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))


# This section is of user 

app.include_router(post.router)

# This is por post 

app.include_router(user.router)

# This is for the authentication route

app.include_router(auth.router)



