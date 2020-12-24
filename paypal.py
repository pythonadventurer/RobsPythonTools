import csv
from pathlib import Path
from time_tools import date_fixer


def paypal_export(paypal_file, export_file):
    with open(Path(paypal_file),encoding='utf-8') as csv_file:
        all_trans = [row for row in csv.reader(csv_file)]

    trans_list = all_trans[1:len(all_trans)]

    trans_export = []

    for row in trans_list:
        trans = []

        # First line of transaction
        trans_line1 = {}

        trans_line1["trans_date"] = date_fixer(row[0])

        if row[3] == "":
            # Don't start trans_description with "_" when there's no name.
            trans_line1["trans_description"] = (row[4] + "_" + row[5])

        else:
            trans_line1["trans_description"] = (row[3] + "_"
                                                + row[4] + "_" + row[5])

        trans_line1["trans_memo"] = ""

        trans_line1["trans_account"] = "Assets:Current Assets:PayPal"

        # "Net" column
        trans_line1["trans_amount"] = float(row[9])

        trans.append(trans_line1)

        # 2nd line of transaction
        trans_line2 = {}

        trans_line2["trans_date"] = ""

        trans_line2["trans_description"] = ""

        trans_line2["trans_memo"] = row[37]

        if "Auction Payment" in trans_line1["trans_description"]:
            # it's an auction payment for a purchase.
            if trans_line1["trans_amount"] <= 0:
                trans_line2["trans_account"] = "Expenses:Uncategorized Expenses"

            # it's a payment received for a sale.
            else:
                trans_line2["trans_account"] = "Income:Current Income:Sales"

        elif "Payment Refund" in trans_line1["trans_description"]:
            trans_line2["trans_account"] = "Income:Current Income:Sales"

        elif "eBay Inc Shipping" in trans_line1["trans_description"]:
            trans_line2["trans_account"] = ("Expenses:"
                                            "Cost of Sales:"
                                            "Shipping Costs")

        elif "Tax collected" in trans_line1["trans_description"]:
            trans_line2["trans_account"] = "Income:Current Income:Sales"

        elif "Certificate Redemption" in trans_line1["trans_description"]:
            trans_line2["trans_account"] = ("Income:"
                                            "Current Income:"
                                            "Rebates & Discounts")

        else:
            trans_line2["trans_account"] = "Expenses:Uncategorized Expenses"

        trans_line2["trans_amount"] = -float(row[7])

        trans.append(trans_line2)

        trans_line3 = {}

        # fee line. Add only if not zero.
        if float(row[8]) != 0:
            trans_line3["trans_date"] = ""

            trans_line3["trans_description"] = ''

            trans_line3["trans_memo"] = row[37]

            trans_line3["trans_account"] = ("Expenses:"
                                            "Cost of Sales:"
                                            "PayPal Fees")

            trans_line3["trans_amount"] = -float(row[8])

            trans.append(trans_line3)

        trans_export.append(trans)

    with open(export_file, 'w', newline='', encoding='utf-8') as csv_file:
        transwriter = csv.writer(csv_file)

        for trans in trans_export:
            for line in trans:
                transwriter.writerow([line["trans_date"],
                                      line["trans_description"],
                                      line["trans_memo"],
                                      line["trans_account"],
                                      line["trans_amount"]])


paypal_export(r"D:\OneDrive\Rob\_Inbox\Download.CSV",
              r"D:\OneDrive\Rob\_Inbox\paypal_export.csv")
