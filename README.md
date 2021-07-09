# Radio Streams VLC

![Chill Streams](images/radio-menu.png)

## Description

This project is a directory of chill electronica streaming radion stations. If you like [DEF CON radio](https://somafm.com/defcon/) or [Groove Salad](https://somafm.com/groovesalad/) on Soma.fm, you know what this is about.

This project provides three things:

1. A directory of streaming radio station URLs
2. A Python API for accessing that directory
3. A command-line utility to launch VLC a selected URLs

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
vlc-radio --help
usage: vlc-radio [-h] [-f] [--no-curses] [station]

positional arguments:
  station            Index or (partial) name of station to play

optional arguments:
  -h, --help         show this help message and exit
  -f, --first-match  Choose first partial station name match
  --no-curses        Disable ncurses interface, run VLC in GUI mode
```
