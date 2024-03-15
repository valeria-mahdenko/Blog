import os
from typing import Any, Callable

import jwt
from datetime import datetime, timedelta

from flask import request, session

from app.constants import JWT_TOKEN_LIFETIME, JWT_GENERATE_ALGORITHM
from app.exceptions import AuthError

secret_key = os.environ.get('SECRET_KEY', 'secret_key')


def generate_jwt(payload: dict, lifetime: int = JWT_TOKEN_LIFETIME) -> str:
    if lifetime:
        payload['exp'] = (datetime.now() + timedelta(minutes=lifetime)).timestamp()
    return jwt.encode(payload, secret_key, algorithm=JWT_GENERATE_ALGORITHM)


def decode_jwt(token: str) -> dict:
    return jwt.decode(token, secret_key, algorithms=[JWT_GENERATE_ALGORITHM])


def check_jwt() -> dict:
    token = request.headers.get('Authorization')
    if not token:
        raise AuthError('Missing access token', status_code=400)
    jwt = token.split('Bearer ')[1]
    try:
        return decode_jwt(jwt)
    except Exception as e:
        raise AuthError(f'Invalid access token: {e}', status_code=401)


def auth_required() -> Callable:
    def _wrapper(route_function: Callable) -> Callable:
        def _decorated_function(*args: Any, **kwargs: Any) -> Any:
            try:
                user_data = check_jwt()
            except AuthError as e:
                raise e
            except Exception as e:
                raise AuthError(f"An error occurred: {e}", status_code=401)

            if 'user_id' not in session or user_data["user_id"] != session['user_id']:
                raise AuthError("Authorization required", status_code=401)

            return route_function(*args, **kwargs)
        _decorated_function.__name__ = route_function.__name__
        return _decorated_function
    return _wrapper
