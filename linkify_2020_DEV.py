from zimwiki import *

links_pages = [r"C:\Users\robf\Documents\Working\Notebooks\DatabaseDocumentation\2020_DEV\Forms.txt",
               r"C:\Users\robf\Documents\Working\Notebooks\DatabaseDocumentation\2020_DEV\Modules.txt",
               r"C:\Users\robf\Documents\Working\Notebooks\DatabaseDocumentation\2020_DEV\Queries.txt",
               r"C:\Users\robf\Documents\Working\Notebooks\DatabaseDocumentation\2020_DEV\Reports.txt",
               r"C:\Users\robf\Documents\Working\Notebooks\DatabaseDocumentation\2020_DEV\Tables.txt"
]

for links_page in links_pages:
    new_page = ZimPage("new_page")

    new_page.read_page(links_page)

    new_page.linkify(links_page)

