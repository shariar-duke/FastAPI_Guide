from typing import List
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..import models, schema, utils
from ..database import get_db


router = APIRouter(
    tags=["Users"]
)

# to create a new user


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):  # type: ignore

    # has the password

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# for getting all the users

@router.get("/users", response_model=List[schema.UserOut])
def test_posts(db: Session = Depends(get_db)):

    users = db.query(models.User).all()
    return users


# get a single user
# to get a single data from the db :

@router.get("/users/{id}", response_model=schema.UserOut)
def get_post(id: int, db: Session = Depends(get_db), ):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id : {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
    return user
