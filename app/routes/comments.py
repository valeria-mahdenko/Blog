from flask import Blueprint, request
from marshmallow import ValidationError

from app import AppError
from app.schemas import CreateCommentInputSchema, CommentSchema
from app.services.auth_handler import auth_required
from app.services import comment_service

comments_bp = Blueprint('comments', __name__)


@comments_bp.route('/comments/<int:post_id>', methods=(['GET', 'POST']))
@auth_required()
def create_or_get_by_post_id(post_id: int):
    if request.method == "POST":
        try:
            comment = CreateCommentInputSchema().load(request.json)
        except ValidationError as err:
            raise AppError(f"An error occurred: {err}", status_code=400)

        comment.post_id = post_id
        created_comment = comment_service.create_comment(comment)
        return CommentSchema().dump(created_comment), 201
    else:
        comments = comment_service.get_comments_by_post_id(post_id)
        return CommentSchema().dump(comments, many=True), 200
