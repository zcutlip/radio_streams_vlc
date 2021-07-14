import time

from typing import List, Tuple

from .cmd import CMD
from .station_list import StationEntry


class VLCException(Exception):
    pass


class VLCLocator(CMD):
    CMD_NAME = "which"
    ARGS = ["vlc"]

    def __init__(self):
        super().__init__(self.ARGS)
        self._location = None

    @property
    def location(self):
        loc = self._location
        if not loc:
            out: bytes
            ret: int
            out, ret = self.run(capture_out=True, capture_err=True)
            out = out.decode("utf-8")
            out = out.rstrip()
            if ret == 0:
                loc = out
                self._location = loc
            else:
                raise VLCException(f"Can't locate VLC: {out}")
        return loc


class VLC(CMD):
    CMD_NAME = "vlc"
    PAUSE_SECS = 2.0

    def __init__(self, entry: StationEntry, ncurses: bool = True, vlc_path: str = None, extra_args: List[str] = []):
        self.entry = entry
        args = [entry.url]
        if ncurses:
            args.extend(["--intf", "ncurses"])
        super().__init__(args)

        if not vlc_path:
            self._location = self._find_vlc()
        else:
            self._location = vlc_path

        self.argv[0] = self._location

    @property
    def location(self):
        return self._location

    def run(self) -> Tuple[bytes, str]:
        self._display_and_pause(self.PAUSE_SECS)
        return super().run()

    def _display_and_pause(self, sec):
        print("")
        print("")
        print(f"Playing: {self.entry.ansi_colorized()}")
        print("")
        print("")
        time.sleep(sec)

    def _find_vlc(self):
        locator = VLCLocator()
        loc = locator.location
        return loc
