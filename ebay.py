from bs4 import BeautifulSoup
from time_tools import date_fixer, timestamp_short
from pathlib import Path
import csv
import os
import shutil
import configparser
from msgbox import MsgBox 


def ebay_active(config_file):
    """
    Extract eBay active listing data from saved HTML and export to CSV.
    """
    config = configparser.ConfigParser()

    config.read(config_file)

    inbox = Path(config["ebay"]["inbox"])

    outbox = Path(config["ebay"]["outbox"])

    filename = config["ebay"]["active_listings_file"]

    foldername = config["ebay"]["active_listings_folder"]

    active_listings_html = Path(inbox,filename)

    # D:\OneDrive\Rob\_Inbox\Manage active listings_files
    active_listings_files = Path(inbox, foldername)

    timestamp = timestamp_short()

    # Folder to save the downloaded html
    # D:\Rob\Finance\2020\eBay\EbayActiveListings\2020-11-14-1822_Active_Listings_html
    html_folder = Path(outbox, "html", timestamp + "_Active_Listings_html").mkdir(parents=True)

    with open(active_listings_html,"r", encoding='utf-8') as f:
        text = f.read()

    soup = BeautifulSoup(text,"html.parser")

    listings = soup.find_all("tr",class_="grid-row")

    # D:\Rob\Finance\2020\eBay\EbayActiveListings\2020-11-14-1822_Active_Listings.csv
    listings_file = Path(outbox, timestamp + "_Active_listings.csv")

    with open(listings_file,"w", 
            newline="", encoding="utf-8") as csv_file:

        writer = csv.writer(csv_file)

        writer.writerow(["title",
                        "price",
                        "purch_option",
                        "views",
                        "watchers",
                        "shipping_cost",
                        "listing_id",
                        "quantity",
                        "starting_price",
                        "start_date",
                        "end_date",
                        "sku"])

        for item in listings:
            title = item.find("div",class_ = "column-title__text" ).get_text()
            
            price = item.find("div",class_ = "col-price__current").get_text().replace("$","")
            
            purch_option = item.find("div",class_ = \
                "col-price__purchase-option").get_text()
            
            views = item.find("td",class_ = \
                "shui-dt-column__visitCount shui-dt--right").get_text()
            
            watchers = item.find("td",class_ = \
                "shui-dt-column__watchCount shui-dt--right").get_text()

            shipping_cost = item.find("td", class_ = \
                "shui-dt-column__shippingCost shui-dt--right").get_text().replace("$","")

            listing_id = item.find("td", class_ = \
                "shui-dt-column__listingId shui-dt--left").get_text()

            quantity = item.find("td", class_ = \
                "shui-dt-column__availableQuantity shui-dt--right editable inline-editable").get_text()

            starting_price = item.find("td", class_ = \
                "shui-dt-column__startingBidPrice shui-dt--right").get_text().replace("$","")

            start_date = item.find("td", class_ = \
                "shui-dt-column__scheduledStartDate shui-dt--left").get_text()        

            start_date = date_fixer(start_date[:start_date.find("at")].strip())

            end_date = item.find("td", class_ = \
                "shui-dt-column__scheduledEndDate shui-dt--left").get_text()

            end_date = date_fixer(end_date[:end_date.find("at")].strip())            

            sku = item.find("td", class_ = \
                "shui-dt-column__listingSKU shui-dt--left editable inline-editable").get_text()

            writer.writerow([title,
                            price,
                            purch_option,
                            views,
                            watchers,
                            shipping_cost,
                            listing_id,
                            quantity,
                            starting_price,
                            start_date,
                            end_date,
                            sku])

    # D:\OneDrive\Rob\_Inbox\Manage active listings.html, 
    # D:\Rob\Finance\2020\eBay\EbayActiveListings\2020-11-14-18-25 Manage active listings_files\
    shutil.copy(Path(active_listings_html),Path(outbox, "html", timestamp + "_Active_Listings_html", filename))

    shutil.copytree(Path(inbox,active_listings_files), Path(outbox,"html", timestamp + "_Active_Listings_html",foldername))

    os.remove(Path(active_listings_html))

    shutil.rmtree(Path(inbox,active_listings_files))

    MsgBox("Import Complete",f"Active Listings have been imported to:\n{listings_file}",0)


def ebay_invoice_export(config_file):
    """
    Export eBay invoice transactions from a downloaded CSV to a format that can be imported into GnuCash.
    The downloaded CSV is renamed with the end date of the applicable month and filed in the eBay folder
    in Finance.  The file for export to GnuCash is save to invoice_export_loc.
    """
    config = configparser.ConfigParser()

    config.read(config_file)

    inbox = Path(config["ebay"]["inbox"])

    # This is where the downloaded CSV will be saved.
    outbox = Path(config["ebay"]["invoice_folder"])

    # This is where the export CSV will be saved.
    invoice_export_file = Path(config["ebay"]["invoice_export_loc"],"ebay_export.csv")

    # Get the path of the downloaded invoice file
    download_file = [file for file in inbox.iterdir()][0]

    # text to include in the downloaded data file when its saved to the eBay invoice data folder
    file_date_text = input("Please enter month end date of invoice in format YYYY-MM-DD: ")

    output_path = Path(outbox, file_date_text + " eBay Transactions.csv")


    # Need to delete all lines up to and including the heading, and the summary lines at the bottom of the file. 
    with open(download_file,encoding='utf-8') as csv_file:
        all_trans = [row for row in csv.reader(csv_file)]

    trans_list = all_trans[8:len(all_trans)-2]

    transactions = []

    for row in trans_list:
        if row != []:

            if row[0] != "":
                trans = []

                trans_line1 = {}

                'Avoid including the PTD time zone in the date parse'
                trans_line1["trans_date"] = date_fixer(row[0][0:9])

                trans_line1["trans_description"] = 'eBay'

                trans_line1["trans_memo"] = ""

                trans_line1["trans_account"] = ("Liabilities:"
                                                "Current Liabilities:"
                                                "eBay Seller Account")

                trans_line1["trans_amount"] = -float(row[4].replace("$",""))

                trans.append(trans_line1)

                # 2nd line of transaction
                trans_line2 = {}

                trans_line2["trans_date"] = ""

                trans_line2["trans_description"] = ""

                trans_line2["trans_memo"] = (row[2] + "_"
                                            + row[3]
                                            + "_"
                                            + row[1].replace("'",""))

                if "Payment" in trans_line2["trans_memo"]:
                    trans_line2["trans_account"] = ("Liabilities:"
                                                    "Current Liabilities:"
                                                    "AAA MasterCard")

                else:
                    trans_line2["trans_account"] = ("Expenses:"
                                                    "Cost of Sales:"
                                                    "eBay Fees")

                trans_line2["trans_amount"] = -trans_line1["trans_amount"]

                trans.append(trans_line2)

                transactions.append(trans)

    with open(invoice_export_file, 'w', newline='',encoding='utf-8') as csv_file:
        transwriter = csv.writer(csv_file)

        for trans in transactions:
            for line in trans:
                transwriter.writerow([line["trans_date"],
                                      line["trans_description"],
                                      line["trans_memo"],
                                      line["trans_account"],
                                      line["trans_amount"]])
    
    shutil.move(download_file, output_path)

    MsgBox("Import Complete",f"Invoice transactions have been imported to:\n{output_path}",0)                                      