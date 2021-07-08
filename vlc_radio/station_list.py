#!/usr/bin/env python
'''Print color-schemed internet radio station list.'''
from csv import reader
from importlib.resources import files

from . import data


DEFAULT_STATIONS_CSV = "stations.csv"
# dark cyan; RGB-format text: 72, 201, 176
ANSI_DK_CY = '\x1b[38;2;72;201;176m'
ANSI_YELO = '\x1b[38;2;244;208;63m'  # yellow
ANSI_DK_ORNG = '\x1b[38;2;220;118;51m'  # dark orange
ANSI_RESET = '\x1b[0m'  # reset text format to default


class StationEntry:

    def __init__(self, name, description, url):
        self._name = name
        self._description = description
        self._url = url

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def url(self):
        return self._url

    def ansi_colorized(self):
        c2 = ANSI_YELO
        c3 = ANSI_DK_ORNG
        res = ANSI_RESET

        line = f'{c2}{self.name:}{res}  {c3}{self.description}{res}'
        return line


class StationList(dict):

    def __init__(self, substring="", first_match=False):
        super().__init__()
        if not substring:
            # first match doesn't make sense if substring is emtpy string
            first_match = False

        try_again = True
        while try_again:
            # If we're doing a substring match, we need to set the try_again flag
            # if not, we shouldn't try again
            try_again = len(substring) > 0
            self._populate_stations(substring, first_match)
            if len(self):
                # found at least one substring match (or no substring was provided)
                break
            # No substring matches, so eliminate the substring
            # TODO: Should we just raise an exception here?
            substring = ""
            continue

        self._exact_match = len(self) == 1

    @property
    def match(self):
        _match = None
        if self._exact_match:
            num = list(self.keys())[0]
            _match = self[num]
        return _match

    def _populate_stations(self, substring, first_match: bool):
        with files(data).joinpath(DEFAULT_STATIONS_CSV).open("r") as _file:
            _reader = reader(_file)
            for number, csv_record in enumerate(_reader, 1):
                name = csv_record[0]
                if substring not in name.lower():
                    continue
                description = csv_record[1]
                url = csv_record[2]
                entry = StationEntry(name, description, url)
                self[number] = entry
                if first_match:
                    break

    def ansi_colorized_line(self, number):
        entry: StationEntry = self[number]
        c1 = ANSI_DK_CY
        res = ANSI_RESET
        colorized_entry = entry.ansi_colorized()

        line = f'{c1}{number:>2}{res}  {colorized_entry}'
        return line

    def print_menu(self):
        for snum in self.keys():
            line = self.ansi_colorized_line(snum)
            print(line)
