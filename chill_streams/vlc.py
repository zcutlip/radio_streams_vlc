import os
import time

from typing import List, Tuple

from .cmd import CMD
from .station_list import StationEntry


class VLCException(Exception):
    pass


class VLCLocator(CMD):
    VLC_PATH_ENV_VAR = "VLC_PATH"
    CMD_NAME = "which"
    ARGS = ["vlc"]

    def __init__(self):
        super().__init__(self.ARGS)
        self._location = self._locate()

    def _locate(self) -> str:
        loc = os.environ.get(self.VLC_PATH_ENV_VAR)
        if loc:
            if not os.path.exists(loc):
                loc = None
        if not loc:
            out: bytes
            ret: int
            out, ret = self.run(capture_out=True, capture_err=True)
            out = out.decode("utf-8")
            out = out.rstrip()
            if ret == 0:
                loc = out
            else:
                raise VLCException(f"Can't locate VLC: {out}")
        return loc

    @property
    def location(self):
        return self._location


class VLC(CMD):
    CMD_NAME = "vlc"
    PAUSE_SECS = 2.0

    def __init__(self, entry: StationEntry, ncurses: bool = True, vlc_path: str = None, extra_args: List[str] = []):
        self.entry = entry
        args = [entry.url]
        if entry.is_video:
            ncurses = False
        if ncurses:
            args.extend(["--intf", "ncurses"])
        else:
            args.extend(["--no-video-title-show", "--meta-title", entry.name])
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
