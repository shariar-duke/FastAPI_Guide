# pylint: disable=import-error, no-name-in-module

from fastapi import Depends, status, HTTPException, APIRouter  # type: ignore
from .. import models, schema, oauth2
from ..database import get_db
from sqlalchemy.orm import Session  # type: ignore

router = APIRouter(
    tags=["Votes"]
)


@router.post("/votes", status_code=status.HTTP_201_CREATED)
def create_vote(
    vote: schema.Vote,
    db: Session = Depends(get_db),
    # current_user is the user ID
    current_user: int = Depends(oauth2.get_current_user)
):
    # Check if the post exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found")  # Fixed typo

    # Check if the vote already exists for this user and post
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user)
    found_vote = vote_query.first()

    # If vote direction is 1, attempt to create a new vote
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user} has already voted on post {vote.post_id}")
        # Create the new vote
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added successfully"}

    # If vote direction is 0, attempt to delete the vote
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote"}
