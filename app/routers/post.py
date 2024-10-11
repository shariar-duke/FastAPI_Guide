from fastapi import FastAPI, Depends , Response, status , HTTPException , APIRouter
from ..import models, schema , utils, oauth2
from ..database import  get_db
from sqlalchemy.orm import Session
from typing import List , Optional
import logging


router = APIRouter(
    tags =["Posts"]
)

# the post request get all the posts from db
@router.get("/posts" , response_model = List[schema.Post])
def test_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    print("I want to get the current user")
    
    # Correct query to query the entire Post model and apply the filter
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts


# to create a new posts
@router.post("/posts", status_code=status.HTTP_201_CREATED , response_model = schema.Post)
def create_posts(post:schema.PostCreate , db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # type: ignore
 
   #print the current user id
   print("I want to printt the current user")
   print(current_user)
   new_post = models.Post(user_id=current_user, **post.dict())
   db.add(new_post)
   db.commit()
   db.refresh(new_post)
   return  new_post


# to get a single data from the db :

@router.get("/posts/{id}", response_model = schema.Post)
def get_post(id:int , db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print("I want to printt the current user")
    print(current_user)
    post = db.query(models.Post).filter(models.Post.id == id).first()
  
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail=f"post with id : {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
    return post


# The delete operation 
@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # Query to find the post by id
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # Handle the case where the post is not found
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    if post.user_id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested acton")

    # Delete the post from the database
    db.delete(post)
    db.commit()

    # Return a 204 No Content response
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update the post 
@router.put("/posts/{id}", status_code=status.HTTP_200_OK , response_model = schema.Post)
def update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db)):

    # Query to find the post by id
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # Handle the case where the post is not found
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    # Update the post with new data
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    # Return the updated post
    return  post_query.first()
