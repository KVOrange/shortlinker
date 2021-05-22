from flask import Flask
from flask_login import LoginManager

import config
from .models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.test' #добавить редирект
    login_manager.init_app(app)

    db.init_app(app)
    with app.test_request_context():
        db.create_all()

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    import app.api.auth as auth
    import app.api.link as link
    import app.api.user as user_req

    app.register_blueprint(auth.module)
    app.register_blueprint(link.module)
    app.register_blueprint(user_req.module)

    return app
