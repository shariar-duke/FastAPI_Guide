from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from .. import models, schema, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login")
def login(user_credentials: schema.UserLogin, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    # Email is found, now compare the password from the database with the user-provided password
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    # At this point, login is successful. Now create a token and send it as a response

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token":  access_token, "token_type": "bearer"}
