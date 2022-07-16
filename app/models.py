from email.policy import default
from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, text
from sqlalchemy.orm import relationship





# class for making table 
class Post(Base):
    # table name
    __tablename__ = 'posts_table'
    
    # table columns
    id = Column(Integer, primary_key=True, nullable = False) # not null
    title = Column(String, nullable = False) 
    content = Column(String, nullable = True)
    published = Column(Boolean, server_default = 'True',  nullable = False)
    create_at = Column(TIMESTAMP(timezone=True), 
                       nullable = False, server_default = text('now()'))
    # relation between table user_login and table post(1 to many). which user creat what posts
    owner_id = Column(Integer, ForeignKey("users_login.id", ondelete="CASCADE"), nullable = False)
    
    # relationship between the User class and Post. we can see information of users who creat a post
    owner = relationship("User")
    
    


# class for making user login table
class User(Base):
    # table name
    __tablename__ = 'users_login'
    
    # table columns
    id = Column(Integer, primary_key=True, nullable = False) # not null
    email = Column(String, nullable = False, unique = True)   
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), 
                       nullable = False, server_default=text('now()'))
    
    
    
# class for making votes table in postgris DB
# this table is using to see which user likes which posts. 
# it hase 2 columns (user_id, post_id). the info of user id we get from users_login table (as foriegnKey) 
# and the info or value for post_id clm we get from posts_table (using its primary key here as foriegn key)
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users_login.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts_table.id", ondelete="CASCADE"), primary_key=True)    
    
   
    
####### command to run server: uvicorn app.main_4:app --reload #########     