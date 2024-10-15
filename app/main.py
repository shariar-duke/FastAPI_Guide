from fastapi import FastAPI, Depends, Response, status, HTTPException
from . import models, schema, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import List
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, user, auth, vote

load_dotenv()

# Create tables
# models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# This section is of user

app.include_router(post.router)

# This is por post

app.include_router(user.router)

# This is for the authentication route

app.include_router(auth.router)

# This is for the vote route

app.include_router(vote.router)
