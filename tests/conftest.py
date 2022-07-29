# it allows us to define fixtures (events which runs before the test starts)
# it alsonmake it possible that this fixtures be usable in all other modules in test directory


# test database 
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db
from app.database import Base
import pytest
from alembic import command
from app import models
from app.oauth2 import creat_access_token



### ======================================= using a new DB for our testing purpose instead using our normal postgres database

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver:port/db"
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

# for postgresql we need just SQLALCHEMY_DATABASE_URL for engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# as far as we now use alembic to create and updates our tables we can commnet this 
Base.metadata.create_all(bind=engine)


# Dependency, making a session during connection with databse
# we overridde this function to make new connection with pgDB for testing 
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# here we override the "get_db" in all methods with "override_get_db" for testing databank         
app.dependency_overrides[get_db] = override_get_db


###################################################################################

# to acces the database obj for manipulating the database during testing 
@pytest.fixture(scope='function')
def session():
     # drope all tables after the test done to prevent error like testing if user already exist for next runing test
     # creat all tables befor running test
     # or using alembic
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    #command.upgrade("head")
    #command.downgrade("base")
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    



# client = TestClient(app)
# we use fixture to run this fun before all other tests
# instead return we use "yield": it gives us the posibility to run code before and after test
@pytest.fixture(scope='function')
def client(session):
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
   

# fixture fo creating new users
@pytest.fixture
def test_user(client):
    user_data = {"email": "user2@gmail.com", 
                 "password": "password123"}
    
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user



# creating acces token for testing posts
@pytest.fixture
def token(test_user):
    return creat_access_token({"user_id": test_user['id']})



# create and authorized_user
@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    
    return client    



# creating a post in DB
@pytest.fixture
def test_posts(test_user, session):
    post_data = [{
        "title": "first post",
        "content": "first content",
        "owner_id": test_user['id']
    },{
        "title": "second post",
        "content": "second content",
        "owner_id": test_user['id']
    },{
        "title": "3rd post",
        "content": "3rd content",
        "owner_id": test_user['id']
    }]    
    
    
    # converting dictionary of all posts to a list to add each post to DB
    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, post_data)
    posts = list(post_map)
    
    # adding all post to DB
    session.add_all(posts)
    session.commit()
    
    # get all posts from database
    posts_db = session.query(models.Post).all()
    
    return posts_db
    