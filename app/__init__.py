from flask import Flask
from flask_jwt_extended import JWTManager

import config
from .models import db, User
front_app = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)
    
    global front_app
    front_app = app
    jwt = JWTManager(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()

    db.init_app(app)
    with app.test_request_context():
        db.create_all()

    import app.api.auth as auth
    import app.api.link as link
    import app.api.user as user_req
    import app.front_api.views as view
    app.register_blueprint(auth.module)
    app.register_blueprint(link.module)
    app.register_blueprint(view.module)
    app.register_blueprint(user_req.module)

    return app
