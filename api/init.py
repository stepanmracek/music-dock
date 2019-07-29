from flask import Flask
from models import db
from redis_client import create_client


def create_app(name):
    app = Flask(name)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:example@db:5432/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app_context().push()
    db.init_app(app)
    db.create_all()

    redis_client = create_client(app)

    return app, redis_client
