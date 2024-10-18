import re

from setuptools import find_packages, setup

about = {}
with open("chill_streams/__about__.py") as fp:
    exec(fp.read(), about)

with open("README.md", "r") as fp:
    long_description = fp.read()


GITHUB_URL = "https://github.com/zcutlip/chill_streams"
# image url: https://github.com/zcutlip/chill_streams/raw/main/images/radio-menu.png
# Image refs on PyPI should have absolute URLs to their home on github
# this awful regex looks for image refs:
#  ![any text](any/image/path), making sure there's no 'http[s]:'
# in the url part
# it then inserts hhttps://github.com/zcutlip/chill_streams/raw/main/
# between the '(' and the relative URL
# source: https://github.com/pypa/readme_renderer/issues/163#issuecomment-1679601106
long_description = re.sub(
    r"(!\[[^\]]+\]\()((?!https?:)[^\)]+)(\))",
    lambda m: m.group(1) + GITHUB_URL + "/raw/main/" +
    m.group(2) + m.group(3),
    long_description,
)

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__summary__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Zachary Cutlip",
    author_email="uid000@gmail.com",
    url="https://github.com/zcutlip/chill_streams",
    license="MIT",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "vlc-radio=chill_streams.cli:main",
            "sltool=chill_streams.cli:sl_main"
        ],
    },

    python_requires=">=3.10",
    install_requires=[
        "python-singleton-metaclasses"
    ],
    extras_require={
        'video-streams': ['streamlink']
    },
    package_data={"chill_streams": ["data/*"]},
)
