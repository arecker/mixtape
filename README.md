# mixtape

Use `mixtape` to build your own mixtapes.

Some features:

- Downloads audio tracks from YouTube or just round them up from local paths
- Automatically converts tracks to OGG format
- Tags final tracks with metadata
- Custom cover art supported!

## Requirements

- `python` (see [.tool-versions](./tool-versions))
- `ffmpeg`
- `make`

## Installation

Just clone this project and run `make`.

If you want, you can create an alias so you can run `mixtape` anywhere.

```
# .bashrc
alias mixtape="$HOME/src/mixtape/venv/bin/mixtape"
```

## Usage

Create a config file.

```yaml
# config.yml
name: My Summer Hits
cover: cover.jpg
tracks:
  - name: Song One
    artist: Artist A
    youtube: https://www.youtube.com/watch?v=example1
  - name: Local Track
    artist: Artist B
    local: tracks/my_song.m4a
```

Run the command.

```
$ mixtape config.yml
```

Your shiny new mixtape will spit out into `./masters/`, metadata included!
