from fastapi import Body, FastAPI,Response, status, HTTPException, Depends, APIRouter
from requests import post
from sqlalchemy.orm import Session
from ..import schemas, database, models, oauth2


# this library helps to have the path operations related to your posts separated from the rest of the code, to keep it organized.
# we can pass also the path as prefix to not to type it for each request.
router = APIRouter(
    prefix="/vote",
    tags=['Vote']  # for grouping the documentation
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), 
         current_user: int = Depends(oauth2.get_current_user)):
    # cheing if a post exist to be voted for 
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} does not exist")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)

    found_vote = vote_query.first()
    # user want to like tha post: 1:already liked (=already exist in vote table) 2:still has not liked(add to vote table) 
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user{current_user.id} has already voted on post {vote.post_id}")
        
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfally added vote"}
    # user want to remove the like of a post(dir=0 or not 1)
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does nit exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        
        return {"message":"successfully deleted vote"}