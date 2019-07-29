#! /usr/bin/env python

from models import Album, Artist, Song, db
from init import create_app
from flask import request, abort, Response
import json


app = create_app(__name__)

# a1 = Artist(name="Artist1")
# b1 = Album(name='Album1', year=2005, artist=a1)
# t1 = Song(track=1, name='song1', album=b1)
# t2 = Song(track=2, name='song2', album=b1)
# t3 = Song(track=3, name='song3', album=b1)
# db.session.add(a1)
# db.session.add(a1)
# db.session.commit()


@app.route('/songs', methods=['GET'])
def get_all_songs():
    return json.dumps([s.to_dict() for s in Song.query.all()]), 200


@app.route('/songs/<int:id>', methods=['GET'])
def get_song(id):
    song = Song.query.get(id)
    return (song.to_dict(), 200) if song else ('Not found', 404)


@app.route('/songs', methods=['POST'])
def add_song():
    if not request.json:
        abort(Response('Request not in JSON format', 400))

    artist_name = request.json.get('artist_name', 'Unknown Artist')
    artist = Artist.query.filter_by(name=artist_name).first()
    if not artist:
        artist = Artist(name=artist_name)
        db.session.add(artist)

    album_name = request.json.get('album_name', 'Unknown Album')
    album = Album.query.filter_by(name=album_name, artist_id=artist.id).first()
    if not album:
        album = Album(name=album_name, year=request.json.get('year'), artist=artist)
        db.session.add(album)

    song = Song(
        track=request.json.get('track'),
        name=request.json.get('name'),
        album=album
    )

    db.session.add(song)
    db.session.commit()
    return json.dumps(song.to_dict()), 200


Song.query.delete()
Album.query.delete()
Artist.query.delete()
db.session.commit()
app.run(debug=True)
