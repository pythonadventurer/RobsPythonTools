from pathlib import Path
from diarium import *
import configparser

config = configparser.ConfigParser()

config_file = "config.ini"

config.read(config_file)

inbox = Path(config["diarium"]["inbox"])

diarium_folder = Path(list(inbox.iterdir())[0])

zim_dest = Path(config["zimwiki"]["notebook"],"2021")

diarium_to_zim(diarium_folder, zim_dest)

