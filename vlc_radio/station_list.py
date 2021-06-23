#!/usr/bin/env python
'''Print color-schemed internet radio station list.'''
from csv import reader
from importlib.resources import files


from . import data

urls = {}  # number selection: station URL


def get_station_list():
    c1 = '\x1b[38;2;72;201;176m'  # dark cyan; RGB-format text: 72, 201, 176
    c2 = '\x1b[38;2;244;208;63m'  # yellow
    c3 = '\x1b[38;2;220;118;51m'  # dark orange
    res = '\x1b[0m'  # reset text format to default

    with files(data).joinpath("stations.csv").open("r") as csv_file:
        csv_rec_list = list(enumerate(reader(csv_file), 1))  # csv reader object
        for num, rec in csv_rec_list:
            print(f'{c1}{num:>2}{res}  {c2}{rec[0]:}{res}  {c3}{rec[1]}{res}')  # station list
            urls[num] = rec[2]  # append number with URL to dictionary
