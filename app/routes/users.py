from flask import Blueprint

from app.schemas import UserSchema
from app.services.auth_handler import auth_required
from app.services import user_service
users_bp = Blueprint('users', __name__)


@users_bp.route('/users/<int:id>', methods=['GET'])
@auth_required()
def get_user_by_id(id: int):
    user = user_service.get_by_id(id)
    schema = UserSchema()
    return schema.dump(user), 200
