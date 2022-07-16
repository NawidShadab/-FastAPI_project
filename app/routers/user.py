from fastapi import Body, FastAPI,Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import engine, get_db


# this library helps to have the path operations related to your posts separated from the rest of the code, to keep it organized.
# we can pass also the path as prefix to not to type it for each request.
router = APIRouter(
    prefix="/users",
    tags=['Users']  # for grouping the documentation
)




# login users
@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.UserOut)
def creat_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    
    # update the user password with overrite it with hashed one
    user.password = hashed_password
    
    # better to convert the pydantic obj to dic and upack it
    new_user = models.User(**user.dict())
    db.add(new_user)    # add new post to DB    
    db.commit() # save the post in DB 
    db.refresh(new_user)    # retun the message, like Returning * 
    
    return new_user


# get user by id
@router.get("/{id}", response_model= schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail=f"User with id: {id} does not exist")
        
    
    return user    