from zimwiki import *

links_pages = [r"C:\Users\robf\Documents\Working\Notebooks\DatabaseDocumentation\Data_Manager_3_DEV\Forms.txt",
               r"C:\Users\robf\Documents\Working\Notebooks\DatabaseDocumentation\Data_Manager_3_DEV\Modules.txt",
               r"C:\Users\robf\Documents\Working\Notebooks\DatabaseDocumentation\Data_Manager_3_DEV\Queries.txt",
               r"C:\Users\robf\Documents\Working\Notebooks\DatabaseDocumentation\Data_Manager_3_DEV\Reports.txt",
               r"C:\Users\robf\Documents\Working\Notebooks\DatabaseDocumentation\Data_Manager_3_DEV\Tables.txt"
]

for links_page in links_pages:
    new_page = ZimPage("new_page")

    new_page.read_page(links_page)

    new_page.linkify(links_page)

