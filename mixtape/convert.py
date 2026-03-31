import base64
import pathlib
import subprocess

from mutagen import id3

from .config import Track


def convert_track(source: str | pathlib.Path, destination: str | pathlib.Path):
    subprocess.run(
        ['ffmpeg', '-i', source, '-codec:a', 'libmp3lame', '-q:a', '2', destination],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def tag_track(target: str | pathlib.Path, track: Track, number: int, album: str, year: int, cover=None):
    tags = id3.ID3()
    tags.add(id3.TIT2(encoding=3, text=track.title))
    tags.add(id3.TPE1(encoding=3, text=track.artist))
    tags.add(id3.TALB(encoding=3, text=album))
    tags.add(id3.TRCK(encoding=3, text=str(number)))
    tags.add(id3.TYER(encoding=3, text=str(year)))

    if cover:
        with open(cover, "rb") as h:
            data = h.read()
        mime = 'image/jpeg'
        if cover.suffix == '.png':
            mime = 'image/png'
        tags.add(id3.APIC(
            encoding=3,
            mime=mime,
            type=3, # front cover
            desc='Cover',
            data=data
        ))

    tags.save(str(target))
