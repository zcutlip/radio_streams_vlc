import os


from . import data
from . import __version__ as chill_streams_version
from .pkg_resources import pkgfiles
from .script_path import get_setuptools_script_dir
from .vlc import VLCLocator, VLCException


class VLCShellScriptException(Exception):
    pass


SCRIPT_TEMPLATE = "vlc-radio-template.sh"


class VLCShellScript:

    def __init__(self):
        self._vlc_path = self._locate_vlc()
        self._vlc_radio_path = self._locate_vlc_radio()

    @staticmethod
    def _locate_vlc():
        locator = VLCLocator()
        try:
            location = locator.location
        except VLCException as e:
            raise VLCShellScriptException(str(e)) from e
        return location

    def _locate_vlc_radio(self):
        script_path = None

        for user_bool in [False, True]:
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
        with pkgfiles(data).joinpath(SCRIPT_TEMPLATE).open("r") as _file:
            template = _file.read()
        return template

    def write_script(self, location):
        location = os.path.expanduser(location)
        location = os.path.normpath(location)
        os.makedirs(location, exist_ok=True, mode=0o755)
        script_path = os.path.join(location, "vlc-radio.sh")
        vlc_dir = os.path.dirname(self._vlc_path)
        radio_cmd = '$_VLC_RADIO_PATH "$@"'
        script_lines = [
            "",
            "# We need to export PATH before doing anything else",
            "# don't put any lines above this",
            f"export PATH=\"${{PATH}}\":{vlc_dir}",
            "",
            "# override default _VLC_RADIO_PATH",
            f"_VLC_RADIO_PATH={self._vlc_radio_path}",
            "# override default _CHILL_STREAMS_VERSION",
            f"_CHILL_STREAMS_VERSION={chill_streams_version}",
            "",
            "update_script && echo_sleep \"Restarting\" 1 && cleanup && exec \"$0\" \"$@\"",
            "",
            radio_cmd,
            ""
        ]
        script_template = self._read_template()
        script = script_template + "\n".join(script_lines)
        with open(os.open(script_path, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o755), "w") as f:
            f.write(script)
