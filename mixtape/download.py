import pathlib
import re

import yt_dlp

from .config import Track


def download_track(track: Track, download_dir: str | pathlib.Path):
    ydl_opts = {
        'quiet': True,
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }],
        'outtmpl': str(pathlib.Path(download_dir) / f'{slugify_track(track)}.%(ext)s'),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(track.youtube)


def slugify_track(track: Track):
    slug = '-'.join([track.artist, track.title])

    # lowercase
    slug = slug.lower()

    # replace spaces with dashes
    slug = slug.replace(' ', '-')

    # remove all extra chars
    r_alpha = re.compile(r'[^a-z0-9\-]')
    return r_alpha.sub('', slug)
