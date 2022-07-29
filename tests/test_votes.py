# testing votes 
import pytest
from app import models

@pytest.fixture()
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[2].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()
    

# testign the votes for a post
def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[2].id, "dir": 1})
    
    assert res.status_code == 201
    
    
# testing a post which is already voted 
def test_vote_twice_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[2].id, "dir": 1})  
    
    assert res.status_code == 409  
    
    
    
# testing a deleting a vote
def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[2].id, "dir": 0})  
    
    assert res.status_code == 201     
    
    
# testing a deleting a vote
def test_delete_vote_non_exist(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[2].id, "dir": 0})  
    
    assert res.status_code == 404 
    


# testing voting a post which is not exist
def test_vote_non_exist_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": 9999999, "dir": 1})  
    
    assert res.status_code == 404         
    
    
    
# testing a unauthorized user  vote a post
def test_vote_unauthorized(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[2].id, "dir": 1})  
    
    assert res.status_code == 401     