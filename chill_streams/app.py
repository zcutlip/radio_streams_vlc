#!/usr/bin/env python
'''Play internet radio selection in VLC media player.
Shift + M --> meta-info; q --> quit'''

import subprocess
import sys

from argparse import ArgumentParser


from .ascii_art import get_ascii_art
from .shell_script import VLCShellScript, VLCShellScriptException
from .station_list import StationEntry, StationList


def vlc_parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "station",
        help="Index or (partial) name of station to play",
        nargs="?",  # make this arg optional
    )
    parser.add_argument(
        "-f", "--first-match",
        help="Choose first partial station name match",
        action="store_true"
    )
    parser.add_argument(
        "--no-curses",
        help="Disable ncurses interface, run VLC in GUI mode",
        action="store_true",
    )

    parsed = parser.parse_args()
    return parsed


def station_selection(options):
    print(get_ascii_art())  # get color-schemed ASCII art heading
    vlc_path = VLCShellScript.locate_vlc()
    '''Play selected internet radio station.'''
    station_text = ""
    station_num = -1
    if options.station:
        try:
            station_num = int(options.station)
        except ValueError:
            station_text = options.station

    station_list = StationList(substring=station_text, first_match=options.first_match)
    entry: StationEntry = station_list.match

    if not entry:
        if station_num < 1:
            station_list.print_menu()
            inp = input('Enter item number: ')
            if inp in ['Q', 'q']:
                return 0
            station_num = int(inp)
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


def vlc_main():
    options = vlc_parse_args()
    if options.write_shell_script:
        try:
            vlcs = VLCShellScript()
            vlcs.write_script("~/.local/bin")
        except VLCShellScriptException as e:
            print(str(e))
            return -1
    else:
        station_selection(options)


if __name__ == '__main__':
    vlc_main()
