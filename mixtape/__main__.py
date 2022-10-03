import argparse
import pathlib


from .download import download


parser = argparse.ArgumentParser()
# parser.add_argument('-g', '--global')
subparsers = parser.add_subparsers(dest='subcommand', required=True)
download_parser = subparsers.add_parser('download', help='download audio files from the internet')
download_parser.add_argument('--url', required=True, help='YouTube video or playlist')


def main():
    args = parser.parse_args()

    match args.subcommand:
        case 'download':
            ensure_dir('downloads')
            download(url=args.url)


def ensure_dir(name: str):
    here = pathlib.Path('.')
    target = here / name
    if not target.is_dir():
        target.mkdir()
