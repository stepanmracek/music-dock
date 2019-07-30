#! /usr/bin/env python

from models import Album, Artist, Song, db
from init import create_app
from flask import request, abort, Response, g
import json


app = create_app(__name__)


def list_response(list):
    return Response(json.dumps([item.to_dict() for item in list]), mimetype='application/json')


def make_query(query, request):
    if request.args:
        return list_response(query.filter_by(**request.args).all())
    else:
        return list_response(query.all())


@app.route('/songs', methods=['GET'])
def get_all_songs():
    return make_query(Song.query, request)


@app.route('/songs/<int:id>', methods=['GET'])
def get_song(id):
    song = Song.query.get(id)
    return (song.to_dict(), 200) if song else ('Song not found', 404)


@app.route('/albums', methods=['GET'])
def get_all_albums():
    return make_query(Album.query, request)


@app.route('/albums/<int:id>', methods=['GET'])
def get_album(id):
    album = Album.query.get(id)
    return (album.to_dict(), 200) if album else ('Album not found', 404)


@app.route('/albums/<int:album_id>/songs', methods=['GET'])
def get_album_songs(album_id):
    songs = Song.query.filter_by(album_id=album_id).order_by(Song.track).all()
    return list_response(songs)


@app.route('/artists', methods=['GET'])
def get_all_artists():
    return make_query(Artist.query, request)


@app.route('/artists/<int:id>', methods=['GET'])
def get_artist(id):
    album = Artist.query.get(id)
    return (album.to_dict(), 200) if album else ('Artist not found', 404)


@app.route('/artists/<int:artist_id>/albums', methods=['GET'])
def get_artist_albums(artist_id):
    albums = Album.query.filter_by(artist_id=artist_id).order_by(Album.year).all()
    return list_response(albums)


@app.route('/songs', methods=['POST'])
def add_song():
    if not request.json:
        abort(Response('Request not in JSON format', 400))

    artist_name = request.json.get('artist_name', 'Unknown Artist')
    artist = Artist.query.filter_by(name=artist_name).first()
    if not artist:
        artist = Artist(name=artist_name)
        db.session.add(artist)
        g.redis.incr('artists')

    album_name = request.json.get('album_name', 'Unknown Album')
    album = Album.query.filter_by(name=album_name, artist_id=artist.id).first()
    if not album:
        album = Album(name=album_name, year=request.json.get('year'), artist=artist)
        db.session.add(album)
        g.redis.incr('albums')

    song = Song(
        track=request.json.get('track'),
        name=request.json.get('name'),
        album=album
    )

    db.session.add(song)
    db.session.commit()
    g.redis.incr('songs')
    return song.to_dict(), 200


@app.route('/songs/<int:id>', methods=['DELETE'])
def delete_song(id):
    song = Song.query.get(id)
    if not song:
        return ('Song not found', 404)
    db.session.delete(song)
    db.session.commit()
    g.redis.decr('songs')
    return f'Deleted {id}', 200


@app.route('/stats', methods=['GET'])
def stats():
    return {
        'artists': int(g.redis.get('artists')),
        'albums': int(g.redis.get('albums')),
        'songs': int(g.redis.get('songs'))
    }, 200

# Song.query.delete()
# Album.query.delete()
# Artist.query.delete()
# db.session.commit()


g.redis.set('artists', Artist.query.count())
g.redis.set('albums', Album.query.count())
g.redis.set('songs', Song.query.count())

if __name__ == '__main__':
    app.run()
