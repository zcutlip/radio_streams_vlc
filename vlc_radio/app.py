#!/usr/bin/env python
'''Play internet radio selection in VLC media player.
Shift + M --> meta-info; q --> quit'''
import os
import sys

from argparse import ArgumentParser
from subprocess import CalledProcessError, run

from .ascii_art import get_ascii_art
from .station_list import StationEntry, StationList


def vlc_parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "station",
        help="Index or (partial) name of station to play.",
        nargs="?",  # make this arg optional
    )
    parser.add_argument(
        "--no-curses",
        help="Disable ncurses interface, run VLC in GUI mode",
        action="store_true",
    )

    parsed = parser.parse_args()
    return parsed


def get_vlc_path():
    SNAP_PATH = '/snap/bin/vlc'
    """
    Temporary hack to support running on other OSes.

    Original project calls abs path to Ubuntu VLC snap,
    so in case that's important, return that if available
    otherwise return just 'vlc'
    """
    vlc_path = 'vlc'
    if os.path.exists(SNAP_PATH):
        vlc_path = SNAP_PATH
    return vlc_path


def station_selection():
    options = vlc_parse_args()
    print(get_ascii_art())  # get color-schemed ASCII art heading
    vlc_path = get_vlc_path()
    '''Play selected internet radio station.'''
    station_text = ""
    station_num = -1
    if options.station:
        try:
            station_num = int(options.station)
        except ValueError:
            station_text = options.station

    station_list = StationList(substring=station_text)
    entry: StationEntry = station_list.match
    if not entry:
        if station_num < 1:
            station_list.print_menu()
            station_num = int(input('Enter item number: '))  # input station number
            entry = station_list[station_num]
        else:
            entry = station_list[station_num]

    vlc_argv = [vlc_path]
    if options.no_curses is False:
        # Use curses unless user specified not to
        # For some reason ncurses is broken on macOS + Apple Silicon + Homebrew VLC cask
        vlc_argv.extend(['--intf', 'ncurses'])

    vlc_argv.append(entry.url)
    print(f"Playing: {entry.ansi_colorized()}")
    print("")
    print("")
    try:
        run(vlc_argv, check=True)  # pass args
    except CalledProcessError as e:
        print(f"Failed to run {vlc_path}", file=sys.stderr)
        return e.returncode
    return 0


if __name__ == '__main__':
    station_selection()
