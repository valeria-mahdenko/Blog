from typing import List

from app import db
from app.exceptions import NotFoundError
from app.models import Comment, Post, User


class CommentService:
    def __init__(self) -> None:
        self._db = db

    def create_comment(self, comment: Comment) -> Comment:
        if not Post.query.get(comment.post_id):
            raise NotFoundError(f"Post with id {comment.post_id} doesn't exist", status_code=400)

        if not User.query.get(comment.author_id):
            raise NotFoundError(f"User with id {comment.author_id} doesn't exist", status_code=400)

        self._db.session.add(comment)
        self._db.session.commit()

        return comment

    def get_comments_by_post_id(self, post_id: int) -> List[Comment]:
        return Comment.query.filter_by(post_id=post_id).all()
