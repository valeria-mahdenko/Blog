from typing import Optional

from app import db, AppError
from app.exceptions import NotFoundError
from app.models import User


class UserService:
    def __init__(self) -> None:
        self._db = db

    def create_user(self, user: User) -> User:
        if User.query.filter_by(email=user.email).first():
            raise AppError("User with these credentials already exists", status_code=400)

        self._db.session.add(user)
        self._db.session.commit()

        return user

    def get_by_id(self, id: int) -> Optional[User]:
        user = User.query.get(id)

        if not user:
            raise NotFoundError(f"User with id {id} does not exist", status_code=401)

        return user
