from flask import Flask
from flask_migrate import MigrateCommand
from .config import Config
from .extensions import db, mail, jwt, migrate
from .user.controllers import user_api
from .post.controllers import post_api
from .product.controllers import product_api
from .comment.controllers import comment_api


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    app.register_blueprint(user_api)
    app.register_blueprint(post_api)
    app.register_blueprint(product_api)
    app.register_blueprint(comment_api)

    return app