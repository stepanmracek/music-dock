from flask import Flask
from models import db


def create_app(name):
    app = Flask(name)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:example@127.0.0.1:5432/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app_context().push()
    db.init_app(app)
    db.create_all()
    return app
