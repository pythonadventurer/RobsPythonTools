from zimwiki import *

links_page = r"C:\Users\robf\Documents\Working\Development\DatabaseAutoDocumentation\2020_DEV\Forms.txt"

new_page = ZimPage("new_page")

new_page.read_page(links_page)

new_page.linkify(links_page)

