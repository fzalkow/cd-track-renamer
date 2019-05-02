# CD Track Renamer

A script to rename audio files of ripped albums according to their song names.

## Requirements

* Python 3
* Working internet connection

## Usage

    $ python rename.py --help
    usage: rename.py [-h] --directory DIRECTORY --artist ARTIST --album ALBUM
                     [--mode MODE]

    Name Audio Files

    optional arguments:
      -h, --help            show this help message and exit
      --directory DIRECTORY
                            album with audio files
      --artist ARTIST       name of artist
      --album ALBUM         name of album
      --mode MODE           test or move (default: test)

The directory should have the following structure:

In case of a single-CD album:

    album-directory/
    ├── track_01.wav
    ├── track_02.wav
    ├── track_03.wav
    ⋮

In case of a multi-CD album:

    album-directory/
    ├── cd1/
    │   ├── track_01.wav
    │   └── track_02.wav
    |   ⋮
    ├── cd2/
    │   ├── track_01.wav
    │   └── track_02.wav
    |   ⋮
    ⋮

## Acknowledgement

This script is based on the [MusicBrainz API](https://musicbrainz.org/doc/Development/XML_Web_Service/Version_2). Thanks to the MusicBrainz community!
