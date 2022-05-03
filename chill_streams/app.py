#!/usr/bin/env python
'''Play internet radio selection in VLC media player.
Shift + M --> meta-info; q --> quit'''

import argparse
import sys

from . import logging

from argparse import ArgumentParser


from .ascii_art import get_ascii_art
from .shell_script import VLCShellScript, VLCShellScriptException
from .station_list import StationEntry, StationList
from .version import CSAbout
from .video_streams import VideoStreamList, VideoStreamDependencyException
from .vlc import VLC


def vlc_parse_args():
    parser = ArgumentParser(description=str(CSAbout()))
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
        "-l", "--loop",
        help="Loop mode: Return to station menu when player terminates (q to quit completely)",
        action="store_true"
    )
    parser.add_argument(
        "--gui",
        help="Disable ncurses interface, run VLC in GUI mode",
        action="store_true",
    )
    parser.add_argument(
        "--write-shell-script",
        help="Write a shell script that sets up environment and executes vlc-radio",
        action="store_true"
    )
    parser.add_argument(
        "--version",
        help="Print version string and exit",
        action='version',
        version=str(CSAbout())
    )
    parser.add_argument(
        # just print the bare version string
        "--bare-version",
        help=argparse.SUPPRESS,
        action='version',
        version=CSAbout().version
    )
    parser.add_argument(
        "--debug", help="Enable debug logging", action='store_true')

    parsed = parser.parse_args()
    return parsed


def station_selection(options):
    print(get_ascii_art())  # get color-schemed ASCII art heading
    '''Play selected internet radio station.'''
    station_text = ""
    station_num = -1
    if options.station:
        try:
            station_num = int(options.station)
        except ValueError:
            station_text = options.station

    go_again = True
    while go_again:
        go_again = False
        station_list = StationList(
            substring=station_text, first_match=options.first_match)
        video_list = {}
        entry: StationEntry = None
        if station_list.match:
            entry = station_list.match
        elif station_list.has_station_num(station_num):
            entry = station_list[station_num]
        else:
            idx = station_list.last_idx + 1
            try:
                # Only create the video stream list if we need to, since it
                # has to hit twitch.tv to query streams
                video_list = VideoStreamList(
                    substring=station_text, first_match=options.first_match, starting_idx=idx)
                if video_list.has_station_num(station_num):
                    entry = video_list[station_num]
                else:
                    entry = video_list.match
            except VideoStreamDependencyException:
                pass

        if not entry:
            all_stations = dict(station_list)
            all_stations.update(video_list)

            station_list.print_menu()
            if video_list:
                video_list.print_menu()
            inp = input('Enter item number [\'q\' to quit]: ')
            if inp in ['Q', 'q']:
                return 0
            station_num = int(inp)
            entry = all_stations[station_num]

        station_text = ""
        station_num = -1

        curses = not options.gui

        vlc = VLC(entry, ncurses=curses)
        _, ret = vlc.run()
        if ret != 0:
            print(f"Failed to run {vlc.location}", file=sys.stderr)
            break
        if options.loop:
            go_again = True

    return ret


def vlc_main():
    options = vlc_parse_args()
    if options.debug:
        logging.enable_debug_logging()

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
