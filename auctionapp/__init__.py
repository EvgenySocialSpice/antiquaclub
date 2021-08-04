from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_required

from auctionapp.user.models import User
from auctionapp.user.views import blueprint as user_blueprint
from auctionapp.site.views import blueprint as site_blueprint
from auctionapp.item.views import blueprint as item_blueprint
from auctionapp.db import db


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    app.register_blueprint(user_blueprint)
    app.register_blueprint(item_blueprint)
    app.register_blueprint(site_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
