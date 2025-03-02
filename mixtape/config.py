import dataclasses
import datetime
import pathlib

import yaml


@dataclasses.dataclass
class Track:
    title: str
    artist: str
    youtube: str = None
    local: str = None


@dataclasses.dataclass
class Config:
    name: str
    year: int
    path: pathlib.Path
    workspace: pathlib.Path
    cover: pathlib.Path
    tracks: list[Track] = dataclasses.field(default_factory=list)


def read_config(path: str) -> Config:
    """Read a mixtape.yml config from path."""

    path = pathlib.Path(path)

    if not path.is_file():
        raise ValueError(f'config file not found: {path}')

    with path.open('r') as f:
        data = yaml.safe_load(f)

    # parse the tracks
    tracks = []
    for item in data.get('tracks', []):
        track = Track(
            title=item['name'],
            artist=item['artist'],
            youtube=item.get('youtube', None),
            local=item.get('local', None),
        )
        tracks.append(track)

    cover = data.get('cover')
    if cover:
        cover = path.parent / cover

    return Config(
        path=path,
        cover=cover,
        year=datetime.datetime.now().year,
        workspace=path.parent,
        name=data['name'],
        tracks=tracks,
    )
