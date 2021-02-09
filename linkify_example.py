from zimwiki import *

links_pages = [r"C:\Users\robf\Documents\my_database\Forms.txt"]


for links_page in links_pages:
    new_page = ZimPage("new_page")

    new_page.read_page(links_page)

    new_page.linkify(links_page)

