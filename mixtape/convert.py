import base64
import pathlib
import subprocess

import mutagen

from .config import Track


def convert_track(source: str | pathlib.Path, destination: str | pathlib.Path):
    subprocess.run(
        ['ffmpeg', '-i', source, '-acodec', 'libvorbis', destination],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def tag_track(target: str | pathlib.Path, track: Track, number: int, album: str, year: int, cover=None):
    f = mutagen.File(str(target))
    f['title'] = track.title.upper()
    f['artist'] = track.artist.upper()
    f['album'] = album.upper()
    f['tracknumber'] = str(number)
    f['year'] = str(year)

    if cover:
        with open(cover, "rb") as h:
            data = h.read()
        picture = mutagen.flac.Picture()
        picture.data = data
        picture.type = 17
        if cover.suffix == '.png':
            picture.mime = 'image/png'
        elif cover.suffix in ['.jpeg', '.jpg']:
            picture.mime = 'image/jpeg'
        picture.width = 100
        picture.height = 100
        picture.depth = 24
        picture_data = picture.write()
        encoded_data = base64.b64encode(picture_data)
        vcomment_value = encoded_data.decode("ascii")
        f["metadata_block_picture"] = [vcomment_value]

    f.save()
