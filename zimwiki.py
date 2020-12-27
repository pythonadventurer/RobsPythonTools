import configparser
import os
import re
from pathlib import Path

config = configparser.ConfigParser()

config.read("config.ini")

nb = Path(config["zimwiki"]["notebook"])

def set_notebook(nb_path):
    config["zimwiki"]["notebook"] = nb_path

    with open("config.ini","w",encoding="utf-8") as config_file:
        config.write(config_file)

    print(f"Notebook set to: {nb_path}")


def set_src(src_path):
    config["zimwiki"]["source"] = src_path

    with open("config.ini","w",encoding="utf-8") as config_file:
        config.write(config_file)

    print(f"Source set to: {src_path}")


class ZimPage:
    def __init__(self):
        self.title = None
        self.parent = None
        self.filename = None
        self.content = None


    def read_page(self, page):
        with open(page,"r",encoding="utf-8") as p:
            self.content = p.read()
        
        re_title = re.compile("====== (.+) ======")

        find_title = re.search(re_title,self.content)

        self.title = find_title.group(1)

        self.filename = Path(page).name

        self.parent = str(Path(page).parent)


    def write_page(self):

        # File name is always derived from the title when writing page
        self.filename = self.title.replace(" ","_") + ".txt"

        with open(Path(self.parent, self.filename),"w",encoding="utf-8") as f:
            f.write(f"====== {self.title} ======\n" + self.content)
        
        print(f"Page saved to: \n{str(Path(self.parent, self.filename))}")
            

my_page = ZimPage()

my_page.read_page(r"D:\OneDrive\Rob\_TO BE FILED\Lifeline\TXT\2018-01-01_Sarasota_and_conversation_wit.txt")

my_page.title = "2018-01-01-0000 Sarasota Conversations"

my_page.parent = Path(config["zimwiki"]["notebook"],"2018")

