from fastapi.testclient import TestClient
from src.main import app
import pytest

client = TestClient(app)

@pytest.fixture
def test_users():
    """Фикстура с тестовыми пользователями"""
    return [
        {'id': 1, 'name': 'Ivan Ivanov', 'email': 'i.i.ivanov@mail.com'},
        {'id': 2, 'name': 'Petr Petrov', 'email': 'p.p.petrov@mail.com'}
    ]

@pytest.fixture(autouse=True)
def setup_db(test_users):
    """Фикстура для инициализации и очистки БД перед каждым тестом"""
    from src.fake_db import db
    db.clear()
    for user in test_users:
        db.create_user(user['name'], user['email'])

def test_get_existed_user(test_users):
    response = client.get("/api/v1/user", params={'email': test_users[0]['email']})
    assert response.status_code == 200
    assert response.json() == {
        'id': test_users[0]['id'],
        'name': test_users[0]['name'],
        'email': test_users[0]['email']
    }

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
    assert isinstance(response.json(), int)  # Проверяем, что возвращается ID

def test_create_user_with_invalid_email(test_users):
    duplicate_user = {
        'name': 'Another Ivan',
        'email': test_users[0]['email']  # Используем существующий email
    }
    response = client.post("/api/v1/user", json=duplicate_user)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}

def test_delete_user(test_users):
    # Удаляем существующего пользователя
    response = client.delete("/api/v1/user", params={'email': test_users[0]['email']})
    assert response.status_code == 204
    
    # Проверяем, что пользователь действительно удален
    check_response = client.get("/api/v1/user", params={'email': test_users[0]['email']})
    assert check_response.status_code == 404