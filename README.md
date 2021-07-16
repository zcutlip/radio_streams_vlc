# Chill Electronica Streams

## Description

This project is a directory of chill electronica streaming radio stations. If you like [DEF CON radio](https://somafm.com/defcon/) or [Groove Salad](https://somafm.com/groovesalad/) on Soma.fm, this is for you.

This project provides three things:

1. A directory of streaming radio station URLs
2. A Python API for accessing that directory
3. A command-line utility to present a menu and launch VLC with a selected URL

## Installation

You can install directly from GitHub:

`pip install --user git+https://github.com/zcutlip/chill_streams.git`

## CLI utility: `vlc-radio`

The `vlc-radio` utility starts up VLC Media Player playing one of the stations in the directory.

It has a few modes of operation:

- VLC running in text (ncurses) mode or GUI mode
- An interactive menu of stations to select from
- Direct play by station number
- Direct play by station name
- If a partial station name is provided and the match is ambiguous, a reduced menu is presented
- First match: if the match is ambiguous, directly play the first option

### CLI Options

```console
usage: vlc-radio [-h] [-f] [--gui] [--write-shell-script] [--version]
                 [station]

Chill Streams: Chill electronica streaming [version 0.1.1.dev0]

positional arguments:
  station               Index or (partial) name of station to play

optional arguments:
  -h, --help            show this help message and exit
  -f, --first-match     Choose first partial station name match
  --gui                 Disable ncurses interface, run VLC in GUI mode
  --write-shell-script  Write a shell script that sets up environment and
                        executes vlc-radio
  --version             Print version string and exit
```

If you just run 'vlc-radio', you get a selection menu of what station to play:
![Chill Streams](images/radio-menu.png)

But, if you already know what station you want, you can ask for it directly:
![Play station 8](images/vlc-radio-8.gif)

If you know the name or partial name of a station, you can ask for it. If the match isn't ambiguous, `vlc` will play the station directly. If it *i*s ambiguous, you'll get a reduced selection list:

![Groove Salad?](images/vlc-radio-groovesalad.gif)

Note that case and whitespace is ignored when asking for a station, so "DEF CON" and "defcon" are equivalent.

If you just want the first match (e.g., "groove salad" not "groove salad classic"), use the `-f` or `--first-match` option:

![first match](images/vlc-radio-groovesalad-first-match.gif)

## Credit

Thanks to [nick3499](https://github.com/nick3499) for the [original project](https://github.com/nick3499/radio_streams_vlc) this is forked from, and for curating a comprehensive directory of shoutcast stations.
