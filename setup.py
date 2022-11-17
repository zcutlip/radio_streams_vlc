from setuptools import find_packages, setup

about = {}
with open("chill_streams/__about__.py") as fp:
    exec(fp.read(), about)

with open("README.md", "r") as fp:
    long_description = fp.read()

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

    python_requires=">=3.8",
    install_requires=[
        "python-singleton-metaclasses",
        # importlib.resources.files requires python >=3.9
        # if python 3.8, need to install 3rd importlib-resources
        "importlib-resources>=5.2.0; python_version<'3.9'"
    ],
    extras_require={
        'video-streams': ['streamlink']
    },
    package_data={"chill_streams": ["data/*"]},
)
