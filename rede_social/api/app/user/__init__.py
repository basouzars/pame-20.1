from flask import Flask
from .app.config import Config
from .app.extensions import db, mail, jwt, migrate
from .app.user.controllers import user_api


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    app.register_blueprint(user_api)

    return app
