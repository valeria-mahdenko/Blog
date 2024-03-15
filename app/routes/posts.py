from flask import Blueprint, request
from marshmallow import ValidationError

from app import AppError
from app.schemas import CreatePostInputSchema, PostSchema
from app.services.auth_handler import auth_required
from app.services import post_service

posts_bp = Blueprint('posts', __name__)


@posts_bp.route('/posts/', methods=(['GET', 'POST']))
@auth_required()
def get_or_create_posts():
    if request.method == "POST":
        try:
            post = CreatePostInputSchema().load(request.json)
        except ValidationError as err:
            raise AppError(f"An error occurred: {err}", status_code=400)

        created_post = post_service.create_post(post)
        return PostSchema().dump(created_post), 201
    else:
        posts = post_service.get_posts()
        return PostSchema().dump(posts, many=True), 200


@posts_bp.route('/posts/<int:id>', methods=['GET'])
@auth_required()
def get_by_id(id: int):
    post = post_service.get_by_id(id)
    return PostSchema().dump(post), 200
