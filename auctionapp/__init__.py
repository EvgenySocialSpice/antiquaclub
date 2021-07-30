from flask import Flask
from auctionapp.user.views import blueprint as user_blueprint
from auctionapp.site.views import blueprint as site_blueprint
from auctionapp.item.views import blueprint as item_blueprint
from auctionapp.db import db


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(item_blueprint)
    app.register_blueprint(site_blueprint)

    return app
