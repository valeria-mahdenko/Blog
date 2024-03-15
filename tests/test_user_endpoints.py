import json
from app import db as _db
from app.models import User


def test_get_user_by_id(client, mock_auth):
    user = User(username='test_user', email='test@example.com')
    user.hash_password("test")
    _db.session.add(user)
    _db.session.commit()

    response = client.get(f'/users/{user.id}')
    assert response.status_code == 200

    user_data = json.loads(response.data)
    assert user_data['username'] == 'test_user'
    assert user_data['email'] == 'test@example.com'


def test_get_user_by_non_existing_id(client, mock_auth):
    response = client.get('/users/999')
    assert response.status_code == 401
