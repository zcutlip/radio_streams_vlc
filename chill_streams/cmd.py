import shlex
import subprocess
from typing import List, Tuple

from .logging import get_logger


class CMD:
    CMD_NAME = None
    ARGS = []

    def __init__(self, argv: List[str] = [], logger=None):
        if logger is None:
            logger = get_logger(__name__)
        self.logger = logger
        if self.CMD_NAME is None:
            raise NotImplementedError("Override CMD_NAME with cmd to run")
        argv = [self.CMD_NAME] + argv
        self.argv = argv

    def run(self, capture_out=False, capture_err=False) -> Tuple[bytes, str]:
        cmd_str = shlex.join(self.argv)
        self.logger.debug(f"About to run: {cmd_str}")
        returncode = 0
        kwargs = {}
        if capture_out:
            kwargs["stdout"] = subprocess.PIPE
        if capture_err:
            kwargs["stderr"] = subprocess.STDOUT

        try:

            p = subprocess.run(self.argv, check=True, **kwargs)
            out = p.stdout
        except subprocess.CalledProcessError as e:
            returncode = e.returncode
            out = e.stdout
        ret = (out, returncode)
        return ret
