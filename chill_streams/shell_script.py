import os
import subprocess

from importlib.resources import files

from . import data
from .script_path import get_setuptools_script_dir


class VLCShellScriptException(Exception):
    pass


SCRIPT_TEMPLATE = "vlc-radio-template.sh"


class VLCShellScript:

    def __init__(self):
        self._vlc_path = self.locate_vlc()
        if not self._vlc_path:
            raise VLCShellScriptException("Unable to locate path to VLC")
        self._vlc_radio_path = self._locate_vlc_radio()

    @staticmethod
    def locate_vlc():
        vlc_path = None
        cmd = ["which", "vlc"]
        try:
            out = subprocess.check_output(cmd)
        except subprocess.CalledProcessError:
            out = None
        if out:
            vlc_path = out.decode("utf-8").strip()
        return vlc_path

    def _locate_vlc_radio(self):
        script_path = None

        for user_bool in [True, False]:
            script_dir = get_setuptools_script_dir(user=user_bool)
            script_path = os.path.join(script_dir, "vlc-radio")
            if os.path.exists(script_path):
                break
            script_path = None
        if not script_path:
            raise VLCShellScriptException("Can't locate script entrypoint")
        return script_path

    def _read_template(self):
        template = ""
        with files(data).joinpath(SCRIPT_TEMPLATE).open("r") as _file:
            template = _file.read()
        return template

    def write_script(self, location):
        location = os.path.expanduser(location)
        location = os.path.normpath(location)
        os.makedirs(location, exist_ok=True, mode=0o755)
        script_path = os.path.join(location, "vlc-radio.sh")
        vlc_dir = os.path.dirname(self._vlc_path)
        radio_cmd = f"{self._vlc_radio_path} \"$@\""
        script_lines = [
            "#!/usr/bin/env sh",
            "",
            "export PATH=\"${{PATH}}\":{}".format(vlc_dir),
            "",
            radio_cmd,
            ""
        ]
        with open(os.open(script_path, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o755), "w") as f:
            f.write("\n".join(script_lines))
