# the schema make us sure that the client send to API the exact piece of DATA that it needs 

from datetime import datetime
import email
from typing import Optional
from pydantic import BaseModel, EmailStr, conint


############################################################        
# schema for creat users login
# which infos wie need to recieve from client as request (request body)
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
# schema for user response
# which info API sends back to client (response body)
class UserOut(BaseModel):
    id: int
    email: EmailStr 
    created_at: datetime   
    
    class Config:
        orm_mode = True
        
        
############################################################
# login Schema
class UserLogin(BaseModel):
    email: EmailStr  
    password: str  
    
    
############################################################
# token Schema
class Token(BaseModel):
    access_token: str
    token_type: str
    
    
class TokenData(BaseModel):
    id: Optional[str] = None
        
        
       

# using data validation (pydantic library) for extracting requests data: "our Schema"
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
# our Schema for creat post (how should the creat post look like). it inherit from PostBase class.    
class PostCreate(PostBase):
    pass


# schema for respons the user
class ResponsPost(PostBase):
    #  can be remove, because we have them in parent class (PostBase)
    # title: str
    # content: str
    # published: bool 
    id: int
    create_at: datetime
    owner_id: int
    owner: UserOut # a pydantic model (info of user who creat the posts)
    
    # this tell paydantic model to read the data even if its not a dict
    class Config:
        orm_mode = True
        
        
# schema for joined tables (post and vote, who voted for a post)        
class PostOut(PostBase):
    Post: ResponsPost
    votes: int
    
    # this tell paydantic model to read the data even if its not a dict
    class Config:
        orm_mode = True
         
        
        
        
# schema for vote (like a post)
# the post_id will be take from JWT Token and its an integer
# the dir can be 0 = delete your like from a post,  or 1= like a post
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
        

