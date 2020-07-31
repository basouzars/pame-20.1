from flask import Flask
from flask_migrate import MigrateCommand
from .config import Config
from .extensions import db, jwt, migrate
from .user.controllers import user_api
from .product.controllers import product_api
from .order.controllers import order_api


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(user_api)
    app.register_blueprint(product_api)
    app.register_blueprint(order_api)

    return app