#!/usr/bin/env python
'''Play internet radio selection in VLC media player.
Shift + M --> meta-info; q --> quit'''
import os

from argparse import ArgumentParser
from subprocess import run

from .ascii_art import get_ascii_art
from .station_list import StationEntry, StationList


def vlc_parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "station_number",
        help="Index of station to play.",
        type=int,
        nargs="?",  # make this arg optional
        default=-1,
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
    station_list = StationList()
    vlc_path = get_vlc_path()
    '''Play selected internet radio station.'''
    station_num = options.station_number
    if station_num < 1:
        station_list.print_menu()
        station_num = int(input('Enter item number: '))  # input station number

    entry: StationEntry = station_list[station_num]

    vlc_argv = [vlc_path]
    if options.no_curses is False:
        # Use curses unless user specified not to
        # For some reason ncurses is broken on macOS + Apple Silicon + Homebrew VLC cask
        vlc_argv.extend(['--intf', 'ncurses'])

    vlc_argv.append(entry.url)
    print(f"Playing: {entry.ansi_colorized()}")
    print("")
    print("")
    run(vlc_argv, check=True)  # pass args


if __name__ == '__main__':
    station_selection()
