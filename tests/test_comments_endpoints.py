import json
from app import db as _db
from app.models import User, Post, Comment


def test_create_comment(client, mock_auth):
    user = User(username='test_user', email='test@example.com')
    _db.session.add(user)
    _db.session.commit()

    post = Post(title='Test Post', content='This is a test post.', author_id=user.id)
    _db.session.add(post)
    _db.session.commit()

    data = {
        "content": "This is a test comment.",
        "author_id": user.id
    }

    response = client.post(f'/comments/{post.id}', json=data)
    assert response.status_code == 201

    comment_data = json.loads(response.data)
    assert comment_data['content'] == 'This is a test comment.'
    assert comment_data['author']['id'] == user.id
    assert comment_data['post']['id'] == post.id


def test_get_comments_by_post_id(client, mock_auth):
    user = User(username='test_user', email='test@example.com')
    _db.session.add(user)
    _db.session.commit()

    post = Post(title='Test Post', content='This is a test post.', author_id=user.id)
    _db.session.add(post)
    _db.session.commit()

    comment1 = Comment(content='Comment 1', author_id=user.id, post_id=post.id)
    comment2 = Comment(content='Comment 2', author_id=user.id, post_id=post.id)

    _db.session.add(comment1)
    _db.session.add(comment2)
    _db.session.commit()

    response = client.get(f'/comments/{post.id}')
    assert response.status_code == 200

    comments_data = json.loads(response.data)
    assert len(comments_data) == 2
    assert comments_data[0]['content'] == 'Comment 1'
    assert comments_data[1]['content'] == 'Comment 2'


def test_get_non_existing_comments_by_post_id(client, mock_auth):
    response = client.get('/comments/999')
    assert response.status_code == 200
    assert len(response.data), 0
