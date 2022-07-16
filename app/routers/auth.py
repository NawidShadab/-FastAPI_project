# Authentication

from fastapi import Body, FastAPI,Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oauth2


# this library helps to have the path operations related to your posts separated from the rest of the code, to keep it organized.
router = APIRouter(
    tags=['Users']  # for grouping the documentation
)

# OAuth2PasswordRequestForm : now we can use form-data in Body (postman) instead rawdat (username, val - password, val)
@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), 
          db: Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid credentials')
    
    # cheking if password is correct an the same as what saved hashed in DB
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f'Invalid credentials')
    
    # creat Token 
    access_token = oauth2.creat_access_token(data= {"user_id": user.id})
    
    
    # return token
    return {"access_token": access_token, "token_type": "bearer"}
    
    
    
    
    