import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver:port/db"
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# for postgresql we need just SQLALCHEMY_DATABASE_URL for engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency, making a session during connection with databse
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
        
# we use sqlachemy to connet to DB, so we dont need it now        
# connencting to postgres DB using psycopg2
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', 
#                                 database='fastapi', 
#                                 user='postgres', 
#                                 password='root',
#                                 cursor_factory=RealDictCursor, 
#                                 )
#         cursor = conn.cursor()
#         print("Databse Connection was succecfull !!!")
#         break
        
#     except Exception as error:
#         print("Connecting to Database failed")    
#         print("Error: ", error) 
#         time.sleep(2)        