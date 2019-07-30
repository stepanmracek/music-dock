from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    artist = db.relationship('Artist', backref=db.backref('albums', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "year": self.year,
            "artist_id": self.artist_id,
            "artist_name": self.artist.name
        }


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(120), nullable=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
    album = db.relationship('Album', backref=db.backref('songs', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "track": self.track,
            "name": self.name,
            "album_id": self.album_id,
            "album_name": self.album.name,
            "artist_id": self.album.artist_id,
            "artist_name": self.album.artist.name,
            "year": self.album.year
        }
