import configparser
from pathlib import Path

config = configparser.ConfigParser()

config.read("config.ini")

nb = Path(config["zimwiki"]["notebook"])

nb_year = Path(nb,"2020")

for item in nb_year.iterdir():
    print(item.name.find("_"))
    