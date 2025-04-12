from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    response = client.get("/api/v1/user", params={'email': "nonexistent@mail.com"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    new_user = {
        'id': 3,
        'name': 'Sergey Sergeev',
        'email': 's.s.sergeev@mail.com'
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    assert response.json() == new_user
    
    response = client.get("/api/v1/user", params={'email': new_user['email']})
    assert response.status_code == 200
    assert response.json() == new_user

def test_create_user_with_invalid_email():
    duplicate_user = {
        'id': 4,
        'name': 'Another Ivan',
        'email': users[0]['email']
    }
    response = client.post("/api/v1/user", json=duplicate_user)
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}

def test_delete_user():
    temp_user = {
        'id': 5,
        'name': 'To Delete',
        'email': 'to.delete@mail.com'
    }
    client.post("/api/v1/user", json=temp_user)
    
    response = client.delete(f"/api/v1/user/{temp_user['id']}")
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}
    
    response = client.get("/api/v1/user", params={'email': temp_user['email']})
    assert response.status_code == 404