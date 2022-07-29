### testing users
import pytest
from app import schemas
from jose import jwt
from app.config import settings







# testing root path
def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == 'Hello workkkkk!'
    assert res.status_code == 200
    

# testing create user: sending the user info through the body of the request as json
def test_create_user(client):
    res = client.post("/users/", json={"email": "user2@gmail.com", "password": "password123"})  
    
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "user2@gmail.com"
    assert res.status_code == 201
    

# we used form-data in body instead of json in postman, so here "data" instead "json"    
def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']}) 
    
    # testing the validation of tokens
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get('user_id')
    
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    
    assert res.status_code == 200
    

# testing invalid login credentialsl
@pytest.mark.parametrize("email, password, status_code",[
    ('wronEmail@gmail.com', 'password123', 403),
    ('user2@gmail.com', 'wrongPassword', 403),
    ('wronEmail@gmail.com', 'wrongPassword', 403),
    (None, 'password123', 422),
    ('user2@gmail.com', None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    
    assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid credentials'
        
        