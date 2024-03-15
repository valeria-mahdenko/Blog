from datetime import datetime
from passlib.hash import pbkdf2_sha256

from app import db


class BaseMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model, BaseMixin):
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    _password_hash = db.Column(db.String)

    posts = db.relationship("Post", back_populates="author", cascade="all, delete",
                            foreign_keys="Post.author_id")

    comments = db.relationship("Comment", back_populates="author", cascade="all, delete",
                               foreign_keys="Comment.author_id")

    def hash_password(self, password):
        self._password_hash = pbkdf2_sha256.hash(password, rounds=20000, salt_size=16)

    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self._password_hash)


class Post(db.Model, BaseMixin):
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    author = db.relationship("User", foreign_keys=[author_id], back_populates="posts")
    comments = db.relationship("Comment", back_populates="post", cascade="all, delete",
                               foreign_keys="Comment.post_id")


class Comment(db.Model, BaseMixin):
    content = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

    author = db.relationship("User", foreign_keys=[author_id], back_populates="comments")
    post = db.relationship("Post", foreign_keys=[post_id], back_populates="comments")
