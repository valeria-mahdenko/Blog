import pytest as pytest

from app import create_app, db as _db
from app.models import User, Post, Comment
from app.routes.auth import auth_bp
from app.routes.comments import comments_bp
from app.routes.posts import posts_bp
from app.routes.users import users_bp


@pytest.fixture(autouse=True)
def client():
    test_app = create_app(config_mode="testing")

    test_app.register_blueprint(auth_bp)
    test_app.register_blueprint(users_bp)
    test_app.register_blueprint(posts_bp)
    test_app.register_blueprint(comments_bp)

    with test_app.test_client() as client:
        with test_app.app_context():
            _db.create_all()
            with client.session_transaction() as sess:
                sess['user_id'] = 1

            yield client
        with test_app.app_context():
            _db.drop_all()


@pytest.fixture
def mock_auth(mocker):
    mocker.patch('app.services.auth_handler.check_jwt', return_value={'user_id': 1})
    mocker.patch('app.services.auth_handler.auth_required', return_value=lambda f: f)


@pytest.fixture
def user():
    return User(username='test_user', email='test@example.com')


@pytest.fixture
def post(user):
    return Post(title='Test Post', content='This is a test post', author=user)


@pytest.fixture
def comment(user, post):
    return Comment(content='Test comment', author=user, post=post)
