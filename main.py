import os

from app import create_app
from app.routes.auth import auth_bp
from app.routes.comments import comments_bp
from app.routes.posts import posts_bp
from app.routes.users import users_bp

app = create_app(os.getenv("CONFIG_MODE", 'dev'))

app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(comments_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
