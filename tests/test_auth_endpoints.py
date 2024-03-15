from app import db as _db
from app.models import User
from werkzeug.datastructures import Headers


def test_register(client):
    data = {
        "username": "test_user",
        "email": "test@example.com",
        "password": "password123"
    }

    response = client.post('/auth/register', json=data)
    assert response.status_code == 201


def test_register_existing_user(client):
    user = User(username='test_user', email='test@example.com')
    user.hash_password("password123")
    _db.session.add(user)
    _db.session.commit()

    data = {
        "username": "test_user",
        "email": "test@example.com",
        "password": "password123"
    }

    response = client.post('/auth/register', json=data)
    assert response.status_code == 400
    assert response.json == {"message": "User with these credentials already exists"}


def test_login(client):
    user = User(username='test_user', email='test@example.com')
    user.hash_password('password123')

    _db.session.add(user)
    _db.session.commit()

    data = {
        "email": "test@example.com",
        "password": "password123"
    }

    response = client.post('/auth/login', json=data)
    assert response.status_code == 200
    assert 'token' in response.json


def test_login_invalid_credentials(client):
    data = {
        "email": "test@example.com",
        "password": "wrong_password"
    }

    response = client.post('/auth/login', json=data)
    assert response.status_code == 400
    assert response.json == {"message": "Invalid credentials"}


def test_logout(client):
    user = User(username='test_user', email='test@example.com')
    user.hash_password('password123')

    _db.session.add(user)
    _db.session.commit()

    data = {
        "email": "test@example.com",
        "password": "password123"
    }

    response = client.post('/auth/login', json=data)
    assert response.status_code == 200
    assert 'token' in response.json

    headers = Headers()
    headers.add('Authorization', f'Bearer {response.json["token"]}')

    response = client.post('/auth/logout', headers=headers)
    assert response.status_code == 204
