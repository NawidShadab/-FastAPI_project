## using an Object relational mapper (ORM) to contact the database
# sqlachemy is a famouse ORM

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

# as far as we now use alembic to create and updates our tables we can commnet this 
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# here we list all domains which are allowed to communicate with our API using a web browser 
# we cann add the urls as string ("https://www.google.com") or using "*" means all domains are allowed to communicate
origins = ["*"]

# https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

        
# send each request to post or user to see where it matches
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router) 

# this message will be displayed when we send a request to localhost port 8000
@app.get("/")
def root():
    return {"message": "Hello workkkkk"}






    

      