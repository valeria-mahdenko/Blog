from flask import Blueprint, request, jsonify, session
from marshmallow import ValidationError

from app import AppError
from app.exceptions import AuthError
from app.models import User
from app.schemas import CreateUserInputSchema
from app.services.auth_handler import generate_jwt, auth_required
from app.services import user_service

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth/register', methods=['POST'])
def register():
    try:
        user = CreateUserInputSchema().load(request.json)
    except ValidationError as err:
        raise AppError(f"An error occurred: {err}", status_code=400)
    user_service.create_user(user)
    return jsonify({"message": "Registration is successful!"}), 201


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    if not email or not password:
        raise AppError("Email or password missing", status_code=400)

    user = User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        session['user_id'] = user.id
        token = generate_jwt(payload={"username": user.username,
                                      "email": user.email,
                                      "user_id": user.id})
        return jsonify({"token": token}), 200
    else:
        raise AuthError("Invalid credentials", status_code=400)


@auth_bp.route('/auth/logout', methods=['POST'])
@auth_required()
def logout():
    if session.get('user_id'):
        session['user_id'] = None
        return jsonify({"message": "You have successfully logged out!"}), 204
    else:
        raise AuthError("Unauthorized", status_code=401)
