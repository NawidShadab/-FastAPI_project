
from fastapi import Body, FastAPI,Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import engine, get_db
from sqlalchemy import func 



# this library helps to have the path operations related to your posts separated from the rest of the code, to keep it organized.
# we can pass also the path as prefix to not to type it for each request.
router = APIRouter(
    prefix="/posts",
    tags=['Posts']  # for grouping the documentation
)


# read all posts from db
#@router.get("/", response_model=List[schemas.PostOut]) # response rout for joined tables
@router.get("/", response_model=List[schemas.ResponsPost])
# making new session, filtering the post number to be showed(limit), skip some posts, search in a post title
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""): 
    # direct sql querya (API <---> DB)
    #cursor.execute("SELECT * FROM posts")
    #posts = cursor.fetchall()
    
    # indirect sending query using ORM (object relational Mapper (sqlachemy) (API <---> ORM <---> DB))
    # making the posts private, like just the owner of the post can see them
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    
    # gell all post. public posts, set limit or skipp some result
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    
    # Join the posts_table and votes table 
    # here is the row sql command: select
    # posts_table.*, count(votes.post_id) as num_likes from posts_table left join votes on posts_table.id = votes.post_id group by posts_table.id
    joined_tables = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # because of a problem with output now not using it.
    
    print("****** here: ****:", joined_tables)
    
    return posts



# creat new post and save it to DB and check if the token is valid (valid user login)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsPost)
def creat_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user),):
    #(API <---> DB)
    """ cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", 
                   (post.title, post.content, post.published))
    
    new_post = cursor.fetchone()
    # save the post in DB
    conn.commit() """
    
    # (API <---> ORM <---> DB))
    # too long to do so if we have 40 columns then so much
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    
    print(current_user.email)
    # better to convert the pydantic obj to dic and upack it
    # using the current loged_in users id as foreignkey(ownewr_id: owner of the created posts)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)    # add new post to DB    
    db.commit() # save the post in DB 
    db.refresh(new_post)    # retun the message, like Returning * 
    return new_post 

 
      
# read specific post which is not exist (ERROR respons)
@router.get("/{id}", response_model= schemas.ResponsPost)
def get_post(id: int, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user),): 
    # (API <---> DB))
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
    # post = cursor.fetchone()
    
    # (API <---> ORM <---> DB))
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    # just the owner of the post can see the post.( private post - not any user who loged in) like delet
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, 
    #                         detail=f'Not authorized to perform requested action')
    
    return post



# delete a post 
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user),):
    # (API <---> DB))
    # cursor.execute("DELETE FROM posts WHERE id = %s returning *", str(id))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    # (API <---> ORM <---> DB))
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    del_post = deleted_post.first()
    
    if del_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} does not exist!!!')
        
    
    # just the owner of the post can delete the post.( not any user who loged in)
    if del_post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, 
                            detail=f'Not authorized to perform requested action')
    
    deleted_post.delete(synchronize_session=False)
    db.commit() 
           
    return Response(status_code=status.HTTP_204_NO_CONTENT)    
    



# Update posts    
@router.put("/{id}", response_model= schemas.ResponsPost)
def update_post(id: int, post:schemas.PostCreate, 
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user),):
    # (API <---> DB)
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
    #                (post.title, post.content, post.published, str(id)))
    
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    # (API <---> ORM <---> DB)
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    up_post = updated_post.first()
    if up_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} does not exist!!!')
        
    
    # just the owner of the post can update the post    
    if up_post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, 
                            detail=f'Not authorized to perform requested action')    
        
    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()    
    return updated_post.first()