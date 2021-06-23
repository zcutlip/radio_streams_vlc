#!/usr/bin/env python
'''Play internet radio selection in VLC media player.
Shift + M --> meta-info; q --> quit'''
import os

from argparse import ArgumentParser
from subprocess import run

from .ascii_art import get_ascii_art
from .station_list import get_station_list, urls


def vlc_parse_args():
    parser = ArgumentParser()
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
    get_station_list()  # list stations
    vlc_path = get_vlc_path()
    '''Play selected internet radio station.'''
    station_num = int(input('Enter item number: '))  # input station number

    vlc_argv = [vlc_path]
    if options.no_curses is False:
        # Use curses unless user specified not to
        # For some reason ncurses is broken on macOS + Apple Silicon + Homebrew VLC cask
        vlc_argv.extend(['--intf', 'ncurses'])

    vlc_argv.append(urls[station_num])
    run(vlc_argv, check=True)  # pass args


if __name__ == '__main__':
    station_selection()
