#! /usr/bin/env python

import os
import sys
import itertools
from mutagen.easyid3 import EasyID3
from collections import namedtuple


Song = namedtuple('Song', ['artist', 'album', 'title', 'track', 'date'])


def crawl(dir, extension):
    def full_path(root, files):
        return (os.path.join(root, file) for file in files if file.endswith('.' + extension))

    nested = (
        full_path(root, files) for root, dir, files in os.walk(dir) if len(files)
    )

    return itertools.chain.from_iterable(nested)


def read_metadata(file):
    def parseTrack(trackString):
        if trackString is str:
            try:
                return int(trackString)
            except ValueError:
                if '/' in trackString:
                    return parseTrack(trackString.split('/')[0])
            except TypeError:
                print(trackString)
        return None

    def parseDate(dateString):
        if dateString:
            try:
                return int(dateString)
            except ValueError:
                pass
            except TypeError:
                print(dateString)
        return None

    id3 = EasyID3(file)
    return Song(
        artist=id3.get('artist'), album=id3.get('album'), title=id3.get('title'),
        track=parseTrack(id3.get('tracknumber')), date=parseDate(id3.get('date'))
    )


def main():
    for dir in sys.argv[1:]:
        print([read_metadata(file) for file in crawl(dir, 'mp3')])


if __name__ == '__main__':
    main()
