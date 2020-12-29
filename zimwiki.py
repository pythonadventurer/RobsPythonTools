import configparser
import os
import re
from pathlib import Path

"""
Zim sub page link example: [[+Add New License Log|Add New License Log]]
"""
config = configparser.ConfigParser()

config.read(r"C:\Users\robf\Documents\Working\Python\RobsPythonTools\config.ini")

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



class ZimPage(object):
    def __init__(self, title):
        self.title = title
        self.parent = nb # Default notebook path from config file
        self.filename = self.title.replace(" ","_") + ".txt"
        self.content = "\n"
        
    def read_page(self, page):
        """
        Replaces title and content with the title and content from
        an existing page.
        """
        with open(page,"r",encoding="utf-8") as p:
            self.content = p.read()
        
        re_title = re.compile("====== (.+) ======")

        find_title = re.search(re_title,self.content)

        self.title = find_title.group(1)
        
        # Strip the title out of the content
        self.content = self.content[find_title.end()+1:]

        self.filename = Path(page).name

        self.parent = str(Path(page).parent)


    def strip_newlines(self):

        # eliminate newlines, except those between paragraphs
        self.content = self.content.replace("\xa0","").split("\n")

        new_content = ""

        for line in self.content:
            if line == "":
                new_content += "\n\n"
           
            else:
                new_content += line + " "

        self.content = new_content


    def linkify(self, page):
        """
        Create a page of links to all of the page's sub pages
        """
        self.read_page(page)

        self.content = ""

        page_path = Path(page)

        subpage_folder = Path(page_path.parent,page_path.stem.replace("_"," "))
        
        for item in subpage_folder.iterdir():
            if item.is_file:
                item_title = item.stem.replace("_"," ")
                
                item_link = f"[[+{item_title}|{item_title}]]\n"

                self.content += item_link

        self.write_page()

    def write_page(self):

        # File name is always derived from the title when writing page
        self.filename = self.title.replace(" ","_") + ".txt"

        with open(Path(self.parent, self.filename),"w",encoding="utf-8") as f:
            f.write(f"====== {self.title} ======\n" + self.content)
        
        print(f"Page saved to: \n{str(Path(self.parent, self.filename))}")
            



