import argparse
import logging
import pathlib
import shutil
import sys

from . import read_config, download_track, slugify_track, convert_track, tag_track


def main():
    args = parse_args()
    logger = make_logger()

    # read config
    config = read_config(args.config)
    logger.info('read config for "%s" with %d track(s)', config.name, len(config.tracks))

    # make sure downloads exist
    download_dir = config.workspace / 'downloads'
    if not download_dir.is_dir():
        download_dir.mkdir()
        logger.info('created downloads directory %s', download_dir)

    # download tracks
    for track in config.tracks:
        if not track.youtube:
            continue
        target = download_dir / f'{slugify_track(track)}.m4a'
        if not target.is_file():
            logger.info('downloading "%s"', track.title)
            download_track(track, download_dir)

    # pave and recreate masters folder
    exports_dir = config.workspace / config.name
    if exports_dir.is_dir():
        shutil.rmtree(exports_dir, )
    exports_dir.mkdir()

    # export tracks
    for i, track in enumerate(config.tracks):
        if track.local:
            source = config.workspace / track.local
        else:
            source = download_dir / f'{slugify_track(track)}.m4a'
        destination = exports_dir / f'{i + 1:02} - {track.title.upper()}.mp3'
        convert_track(source, destination)
        logger.info('converting "%s" [%d/%d]', track.title, i + 1, len(config.tracks))

    # tag tracks
    for i, track in enumerate(config.tracks):
        target = exports_dir / f'{i + 1:02} - {track.title.upper()}.mp3'
        logger.info('tagging "%s" [%d/%d]', track.title, i + 1, len(config.tracks))
        tag_track(target, track, i + 1, config.name, config.year, cover=config.cover)


def parse_args():
    parser = argparse.ArgumentParser('mixtape', description='The scrappy cli mixtape builder.')
    parser.add_argument('config', help='path/to/config.yml', type=pathlib.Path)
    return parser.parse_args()


def make_logger() -> logging.Logger:
    logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter('mixtape: %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


if __name__ == '__main__':
    main()
