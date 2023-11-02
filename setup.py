from setuptools import setup, find_packages

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
)
