from typing import List, Optional

from app import db
from app.exceptions import NotFoundError
from app.models import Post, User


class PostService:
    def __init__(self) -> None:
        self._db = db

    def create_post(self, post: Post) -> Post:
        if not User.query.get(post.author_id):
            raise NotFoundError(f"User with id {post.author_id} doesn't exist", status_code=400)

        self._db.session.add(post)
        self._db.session.commit()

        return post

    def get_posts(self) -> List[Post]:
        return Post.query.all()

    def get_by_id(self, id: int) -> Optional[Post]:
        post = Post.query.get(id)
        if not post:
            raise NotFoundError(f"Post with id {id} doesn't exist", status_code=400)

        return post
