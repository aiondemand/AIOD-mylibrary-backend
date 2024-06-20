import pathlib
import toml
import os


with open(pathlib.Path(__file__).parent / "config.toml", "r") as fh:
    CONFIG = toml.load(fh)


DB_CONFIG = CONFIG.get("database", {})
