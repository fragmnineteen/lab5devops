from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_get_existed_user():
    response = client.get("/api/v1/user", params={'email': 'i.i.ivanov@mail.com'})
    assert response.status_code == 200
    data = response.json()
    assert data['email'] == 'i.i.ivanov@mail.com'
    assert data['name'] == 'Ivan Ivanov'

def test_get_unexisted_user():
    response = client.get("/api/v1/user", params={'email': "nonexistent@mail.com"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    new_user = {
        'name': 'Sergey Sergeev',
        'email': 's.s.sergeev@mail.com'
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    assert isinstance(response.json(), int)

def test_create_user_with_invalid_email():
    duplicate_user = {
        'name': 'Another Ivan',
        'email': 'i.i.ivanov@mail.com'  # Используем существующий email
    }
    response = client.post("/api/v1/user", json=duplicate_user)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}

def test_delete_user():
    # Сначала создаём пользователя для удаления
    client.post("/api/v1/user", json={
        'name': 'To Delete', 
        'email': 'to.delete@mail.com'
    })
    
    # Удаляем его
    response = client.delete("/api/v1/user", params={'email': 'to.delete@mail.com'})
    assert response.status_code == 204
    
    # Проверяем удаление
    check_response = client.get("/api/v1/user", params={'email': 'to.delete@mail.com'})
    assert check_response.status_code == 404
