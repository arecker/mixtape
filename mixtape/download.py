import collections
import contextlib
import os
import pathlib
import re
import shutil
import tempfile

import slugify
import yt_dlp


def download(url=None):
    here = pathlib.Path('.').absolute()
    download_dir = here / 'downloads'
    with in_temp_directory() as temp_dir:
        with yt_dlp.YoutubeDL({'format': 'm4a/bestaudio/best', 'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=True)
            info = extract_video_info(info['title'])
            source = list(temp_dir.glob('*.m4a'))
            assert len(source) == 1, f'expected one result in {source}'
            source = source[0]
            # copy the file out
            shutil.copy(source, download_dir / f'{info.slug}.m4a')
            print(f'downloaded {info.slug}.m4a')


@contextlib.contextmanager
def in_temp_directory():
    here = pathlib.Path('.').absolute()
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        try:
            yield pathlib.Path(temp_dir)
        finally:
            os.chdir(here)


VideoInfo = collections.namedtuple('VideoInfo', 'artist title slug')


def extract_video_info(video_title: str) -> VideoInfo:
    artist, title = None, None

    if match := re.fullmatch(r'^(?P<artist>.*) - (?P<title>.*?)(\s\(Official Music Video\))$', video_title):
        artist, title = match.group('artist'), match.group('title')
    elif match := re.fullmatch(r'^(?P<artist>.*) - (?P<title>.*?)(\sft\..*)$', video_title):
        artist, title = match.group('artist'), match.group('title')

    if not all([artist, title]):
        raise ValueError(f'could not artist/title match "{video_title}"!')

    title, artist = title.lower(), artist.lower()
    slug = slugify.slugify(artist) + '-' + slugify.slugify(title)
    return VideoInfo(artist=artist, title=title, slug=slug)
