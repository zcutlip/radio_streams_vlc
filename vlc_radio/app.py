#!/usr/bin/env python
'''Play internet radio selection in VLC media player.
Shift + M --> meta-info; q --> quit'''
from subprocess import run

from .ascii_art import get_ascii_art
from .station_list import get_station_list


def station_selection():
    print(get_ascii_art())  # get color-schemed ASCII art heading
    get_station_list()  # list stations

    '''Play selected internet radio station.'''
    urls = station_list.urls  # obj: number/station name/genres/url
    station_num = int(input('Enter item number: '))  # input station number
    run(['/snap/bin/vlc', '--intf', 'ncurses', urls[station_num]], check=True)  # pass args


if __name__ == '__main__':
    station_selection()
