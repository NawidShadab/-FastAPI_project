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
   
