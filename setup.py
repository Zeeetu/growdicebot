import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

with (HERE / "requirements.txt").open() as f:
    requirements = f.read().splitlines()

setup(
    name="growdicebot",
    version="1.0.0",
    description="Bot for GrowDice.net",
    packages=find_packages(),
    author="zeeetu",
    entry_points={
        "console_scripts": [
            "growdicebot = growdicebot.cli:main",
        ],
    },
    install_requires=requirements,
)
