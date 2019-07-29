#! /usr/bin/env python

import os
import sys
import itertools
import requests
import json
from mutagen.easyid3 import EasyID3
from collections import namedtuple


Song = namedtuple('Song', ['artist_name', 'album_name', 'name', 'track', 'date'])


def crawl(dir, extension):
    def full_path(root, files):
        return (
            os.path.join(root, file) for file in files if file.endswith('.' + extension)
        )

    nested = (
        full_path(root, files) for root, dir, files in os.walk(dir) if len(files)
    )

    return itertools.chain.from_iterable(nested)


def read_metadata(file):
    def get(tagValue):
        if isinstance(tagValue, list):
            return tagValue[0] if len(tagValue) else None
        return tagValue

    def parse_track(track):
        if isinstance(track, str):
            try:
                return int(track)
            except ValueError:
                if '/' in track:
                    return parse_track(track.split('/')[0])
            except TypeError:
                print('parse error of %s' % track)
        return None

    def parse_date(date):
        try:
            return int(date)
        except (ValueError, TypeError):
            print('parse error of %s' % date)
        return None

    id3 = EasyID3(file)
    return Song(
        artist_name=get(id3.get('artist')),
        album_name=get(id3.get('album')),
        name=get(id3.get('title')),
        track=parse_track(get(id3.get('tracknumber'))),
        date=parse_date(get(id3.get('date')))
    )


def main():
    for dir in sys.argv[1:]:
        for file in crawl(dir, 'mp3'):
            metadata = read_metadata(file)
            print(metadata)

            try:
                headers = {"Content-Type": "application/json"}
                payload = json.dumps(metadata._asdict())
                print(payload)
                response = requests.post('http://127.0.0.1:5000/songs', data=payload, headers=headers)
                print(response.text)
            except Exception as e:
                print('Error when uploading', metadata, e)


if __name__ == '__main__':
    main()
