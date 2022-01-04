import re
from argparse import ArgumentParser
from csv import reader
from .pkg_resources import pkgfiles

from . import data
from .url import URL

DEFAULT_STATIONS_CSV = "stations.csv"
# dark cyan; RGB-format text: 72, 201, 176
ANSI_DK_CY = '\x1b[38;2;72;201;176m'
ANSI_YELO = '\x1b[38;2;244;208;63m'  # yellow
ANSI_DK_ORNG = '\x1b[38;2;220;118;51m'  # dark orange
ANSI_RESET = '\x1b[0m'  # reset text format to default


class StationListParseException(Exception):
    pass


class StationEntry:

    def __init__(self, name, description, url, is_video):
        self._name = name
        self._description = description
        self._url = URL(url)
        self._is_video = is_video

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def url(self):
        return str(self._url)

    @property
    def is_video(self):
        return self._is_video

    @property
    def port(self):
        return self._url.parsed.port

    def ansi_colorized(self):
        c2 = ANSI_YELO
        c3 = ANSI_DK_ORNG
        res = ANSI_RESET

        line = f'{c2}{self.name:}{res}  {c3}{self.description}{res}'
        return line


class StationList(dict):
    LIST_NAME = "Streaming Audio Channels"
    STATION_CSV = DEFAULT_STATIONS_CSV
    VIDEO_STREAMS = False

    def __init__(self, substring="", first_match=False, starting_idx=1):
        super().__init__()
        self._starting_idx = starting_idx
        if not substring:
            # first match doesn't make sense if substring is emtpy string
            first_match = False

        try_again = True
        while try_again:
            # If we're doing a substring match, we need to set the try_again flag
            # if not, we shouldn't try again
            try_again = len(substring) > 0
            self._populate_stations(substring, starting_idx, first_match)
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

    @property
    def last_idx(self):
        return self._starting_idx + len(self) - 1

    def _collapse_string(self, strarg):
        """
        Collapse all whitespace out of a string,
        and normalize to lower case
        """
        rex = re.compile(r'\W+')
        result = rex.sub('', strarg)
        result = result.lower()
        return result

    def has_station_num(self, station_num):
        return station_num in self.keys()

    def parse_csv_record(self, csv_record: list):
        try:
            name = csv_record[0]
            description = csv_record[1]
            url = csv_record[2]
        except IndexError as e:
            raise StationListParseException(
                "Unable to parse name, description, and URL from CSV record") from e
        return (name, description, url)

    def _populate_stations(self, substring, starting_idx, first_match: bool):
        substring = self._collapse_string(substring)
        with pkgfiles(data).joinpath(self.STATION_CSV).open("r") as _file:
            _reader = reader(_file)
            for number, csv_record in enumerate(_reader, starting_idx):
                try:
                    name, description, url = self.parse_csv_record(csv_record)
                except StationListParseException:
                    print(f"failed to parse {csv_record}")
                    continue
                if name.startswith("?"):
                    continue

                _name = self._collapse_string(name)
                if substring not in _name:
                    continue
                entry = StationEntry(
                    name, description, url, self.VIDEO_STREAMS)
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

    def print_header(self):
        top_bottom = "=" * (len(self.LIST_NAME) + 4)
        # ============================
        # *                          *
        # * Streaming Audio Channels *
        # *                          *
        # ============================
        lines = [
            top_bottom,
            "*" + " " * (len(top_bottom) - 2) + "*",
            "* " + self.LIST_NAME + " *",
            "*" + " " * (len(top_bottom) - 2) + "*",
            top_bottom
        ]
        for line in lines:
            print(line)

    def print_menu(self):
        self.print_header()
        for snum in self.keys():
            line = self.ansi_colorized_line(snum)
            print(line)


def sl_parse_args():
    parser = ArgumentParser()
    subp = parser.add_subparsers()
    url_cmd = subp.add_parser("print-stations")
    url_cmd.add_argument("--urls", action="store_true")
    url_cmd.add_argument("--nonstandard-ports", action="store_true")

    parsed = parser.parse_args()
    return parsed


def station_list_main():
    config = sl_parse_args()
    station_list = StationList()
    if config.urls:
        ignore_ports = []
        if config.nonstandard_ports:
            ignore_ports = [80, 443, None]
        for _, station_entry in station_list.items():
            url = station_entry.url
            if station_entry.port not in ignore_ports:
                print(url)
