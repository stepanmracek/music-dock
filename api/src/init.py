from flask import Flask, g
from models import db
from redis_client import create_client
from database import DATABASE_CONNECTION_URI
from flask_cors import CORS


def create_app(name):
    app = Flask(name)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app_context().push()
    db.init_app(app)
    db.create_all()

    g.redis = create_client(app)

    return app
