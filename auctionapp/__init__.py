from flask import Flask
from auctionapp.models_db import Base


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    Base.init_app(app)

    @app.route('/')
    def hello_world_page():
        return "Hello world!"

    return app
