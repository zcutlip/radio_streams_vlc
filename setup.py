from setuptools import find_packages, setup

about = {}
with open("chill_streams/__about__.py") as fp:
    exec(fp.read(), about)

with open("README.md", "r") as fp:
    long_description = fp.read()

setup(
    name="chill-streams",
    version=about["__version__"],
    description=about["__summary__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="",
    author_email="",
    url="TBD",
    license="MIT",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["vlc-radio=chill_streams.cli:main"],
    },
    python_requires=">=3.7",
    install_requires=[],
    package_data={"chill_stations": ["data/*"]},
)
