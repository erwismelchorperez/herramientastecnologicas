from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

login_manager = LoginManager()

def create_app():

    app = Flask(__name__)

    app.config.from_object('config.Config')

    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):

        return User.query.get(int(user_id))

    # IMPORTS
    from app.routes.auth import auth
    from app.routes.dashboard import dashboard
    from app.routes.cartera import cartera
    from app.routes.captacion import captacion
    from app.routes.api import api
    from app.routes.socios import socios
    from app.routes.forecast_cartera import forecast_cartera

    # BLUEPRINTS
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(cartera)
    app.register_blueprint(captacion)
    app.register_blueprint(api)
    app.register_blueprint(socios)
    app.register_blueprint(forecast_cartera)

    return app