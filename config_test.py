import configparser
from pathlib import Path

config = configparser.ConfigParser()

config.read(r"C:\Users\robf\Documents\Working\Python\RobsPythonTools\config.ini")

nb = Path(config["zimwiki"]["notebook"])