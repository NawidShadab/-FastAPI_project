# testing posts

# testing get all posts by authorized_users (authorized_client)
from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


# testing if get all posts by unauthorized_users (client) doesnt work
def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")  
    
    assert res.status_code == 401
    
    
# testing if get one posts by unauthorized_users (client) doesnt work
def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 401    
    


# test a post which is not exists in the db
def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{999999}")  
    
    assert res.status_code == 404
    
    
#  testing getting one post with authorized_users
def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}") 
    post = schemas.ResponsPost(**res.json())

    assert post.id == test_posts[0].id
    assert post.content == test_posts[0].content


# testing create posts
@pytest.mark.parametrize("title, content, published", [
    ("title 1", "contetnt 1", True),
    ("title 2", "contetnt 2", False),
    ("title 3", "contetnt 3", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    
    create_post = schemas.ResponsPost(**res.json())
    
    assert res.status_code == 201
    assert create_post.title == title
    assert create_post.content == content
    assert create_post.published == published
    assert create_post.owner_id == test_user ['id']



# test if unauthorized_users can create posts 
def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json={"title":"title not allowed", "content":"content not allowed"})  
    
    assert res.status_code == 401

    

# testing if unauthorized_users can delete posts
def test_unauthorized_user_delete_post(client, test_posts, test_user):
    res = client.delete(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 401
    
 
    
# testing if authorized_users can delete a posts
def test_delete_post_success(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 204



# testing deleting non exist post
def test_delet_non_existent_post(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/999999")
    
    assert res.status_code == 404       
    
    
    
# testing update a post succes
def test_update_post(authorized_client, test_posts, test_user):
    data = {
        "title": "update title",
        "content": "update content",
        "id": test_posts[0].id,
    }    
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.ResponsPost(**res.json())
    
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]
    
    

# testing if unauthorized_users can update posts
def test_unauthorized_user_update_post(client, test_posts, test_user):
    res = client.put(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 401    
    
    
    
# testing updating non exist post
def test_update_non_existent_post(authorized_client, test_posts, test_user):
    data = {
        "title": "update title",
        "content": "update content",
        "id": test_posts[0].id,
    } 
    res = authorized_client.put(f"/posts/88888", json=data)
    
    assert res.status_code == 404      