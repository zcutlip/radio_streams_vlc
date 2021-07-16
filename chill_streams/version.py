from . import __summary__, __title__, __version__


class CSAbout:
    def __init__(self):
        self.version = __version__
        self.summary = __summary__
        self.title = __title__

    def __str__(self):
        return f"{self.title}: {self.summary} [version {self.version}]"
