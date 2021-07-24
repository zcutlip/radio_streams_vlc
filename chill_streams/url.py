import urllib
from pysingleton import PySingleton

from . import data
from .pkg_resources import pkgfiles

"""
HTTPS upgrading
This module allows us to upgrade certain URLs to HTTPS if their domain is on the
list of domains known to support TLS.

This makes it possible to continue updating 'stations.csv' from upstream or other
sources but also upgrade to HTTPS where possible

TODO: handle URLs that are IP address only
TODO: handle URLs that are on ports other than 80 that support HTTPS on a port other than 443
"""


class HTTPSDomainList(list, metaclass=PySingleton):
    # TODO: Make this a singleton
    HTTPS_FILE = "https.txt"

    def __init__(self):
        super().__init__()
        with pkgfiles(data).joinpath(self.HTTPS_FILE).open("r") as _file:
            line: str
            for line in _file.readlines():
                if line.startswith("#"):
                    continue
                line = line.rstrip()
                if not line:
                    # skip empty lines
                    continue
                self.append(line)


class URL:
    def __init__(self, url_string):
        parsed = urllib.parse.urlparse(url_string)
        domain_list = HTTPSDomainList()
        self.parsed = self._https_upgrade(parsed, domain_list)

    def _https_upgrade(self, parsed_url, domain_list):
        netloc: str = parsed_url.netloc
        parts = netloc.split(":")
        hostname = parts.pop(0)
        port = parts.pop() if parts else None
        if port == "80":
            port = None
            parsed_url = parsed_url._replace(netloc=hostname)

        parts = hostname.split(".")
        domain = ".".join(parts[-2:])
        if domain in domain_list:
            if port is None:
                parsed_url = parsed_url._replace(scheme="https")
        return parsed_url

    def __str__(self):
        return urllib.parse.urlunparse(self.parsed)
