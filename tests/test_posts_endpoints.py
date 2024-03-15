import json
from app import db as _db
from app.models import User, Post


def test_create_post(client, mock_auth):
    user = User(username='test_user', email='test@example.com')
    _db.session.add(user)
    _db.session.commit()

    data = {
        "title": "Test Post",
        "content": "This is a test post.",
        "author_id": user.id
    }

    response = client.post('/posts/', json=data)
    assert response.status_code == 201

    post_data = json.loads(response.data)
    assert post_data['title'] == 'Test Post'
    assert post_data['content'] == 'This is a test post.'
    assert post_data['author']['id'] == user.id


def test_get_all_posts(client, mock_auth):
    user = User(username='test_user', email='test@example.com')
    _db.session.add(user)
    _db.session.commit()

    post1 = Post(title='Post 1', content='Content 1', author_id=user.id)
    post2 = Post(title='Post 2', content='Content 2', author_id=user.id)
    _db.session.add(post1)
    _db.session.add(post2)
    _db.session.commit()

    response = client.get('/posts/')
    assert response.status_code == 200

    posts_data = json.loads(response.data)
    assert len(posts_data) == 2
    assert posts_data[0]['title'] == 'Post 1'
    assert posts_data[1]['title'] == 'Post 2'


def test_get_post_by_id(client, mock_auth):
    user = User(username='test_user', email='test@example.com')
    _db.session.add(user)
    _db.session.commit()

    post = Post(title='Test Post', content='This is a test post.', author_id=user.id)
    _db.session.add(post)
    _db.session.commit()

    response = client.get(f'/posts/{post.id}')
    assert response.status_code == 200

    post_data = json.loads(response.data)
    assert post_data['title'] == 'Test Post'
    assert post_data['content'] == 'This is a test post.'
    assert post_data['author']['id'] == user.id


def test_get_post_by_non_existing_id(client, mock_auth):
    response = client.get('/posts/999')
    assert response.status_code == 400
