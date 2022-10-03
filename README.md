# mixtape

The nifty little CLI mixtape builder for weirdos like me.

## Install

Run make in this directory.

```
$ make
rm -rf ./venv
python -m venv --copies ./venv
./venv/bin/pip install --upgrade --quiet pip
./venv/bin/pip install -r requirements.txt --quiet
```

Create a symlink to the `mixtape` script to your local bin.

```
$ ln -s ~/src/mixtape/venv/bin/mixtape ~/bin/mixtape
```

## Usage

### `mixtape download`

Download files from the Internet.  These are saved to a `downloads` directory.

```
$ mixtape download --url "https://youtu.be/dQw4w9WgXcQ?si=KsElUPtx_ADfEokt"
downloaded rick-astley-never-gonna-give-you-up.m4a
```

## Testing

- Run `make dev` to install fancy pip packages
- Run `make test` to run all 1 of my unit tests
