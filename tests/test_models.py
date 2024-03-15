from app import db as _db
from app.models import User, Post, Comment


def test_user_creation(user):
    _db.session.add(user)
    _db.session.commit()

    assert User.query.filter_by(username='test_user').first() == user


def test_post_creation(post):
    _db.session.add(post)
    _db.session.commit()

    assert Post.query.filter_by(title='Test Post').first() == post


def test_comment_creation(comment):
    _db.session.add(comment)
    _db.session.commit()

    assert Comment.query.filter_by(content='Test comment').first() == comment


def test_user_password_hashing():
    user = User()
    password = 'test_password'
    user.hash_password(password)
    assert user.verify_password(password)


def test_user_password_verification():
    user = User()
    password = 'test_password'
    user.hash_password(password)
    assert user.verify_password('wrong_password') is False
