#! /usr/bin/env python

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=True)


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    artist = db.relationship('Artist', backref=db.backref('albums', lazy=True))


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(120), nullable=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
    album = db.relationship('Album', backref=db.backref('songs', lazy=True))


db.create_all()

a1 = Artist(name="Artist1")
b1 = Album(name='Album1', year=2005, artist=a1)
t1 = Song(track=1, name='song1', album=b1)
t2 = Song(track=2, name='song2', album=b1)
t3 = Song(track=3, name='song3', album=b1)
db.session.add(a1)
db.session.add(a1)
db.session.commit()
