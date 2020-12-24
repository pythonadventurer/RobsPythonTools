import sqlite3
import csv
from msgbox import MsgBox

def gnucash_export(gnucash_db,output_file):
    """
    Export GnuCash transactions from a sqlite3-based GnuCash file to CSV.
    """
    gnucash_query = """SELECT transactions.guid,
        transactions.post_date, 
        transactions.num, 
        transactions.description, 
        splits.action,
        splits.memo, 
        parent_accts.name AS parent_acct, 
        accounts.name AS acct, 
        splits.value_num
    FROM (transactions 
    INNER JOIN splits ON transactions.guid = splits.tx_guid) 
    INNER JOIN (accounts LEFT JOIN accounts AS parent_accts ON accounts.parent_guid = parent_accts.guid) ON splits.account_guid = accounts.guid;"""

    with sqlite3.connect(gnucash_db) as connection:
        cursor = connection.cursor()
        cursor.execute(gnucash_query)
        trans_list = [row for row in cursor.fetchall()]

    with open(output_file,"w",encoding='utf-8',newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["guid","post_date","num","description","sku","memo","parent_acct","acct","value_num"])
        for row in trans_list:
            writer.writerow(row)

    MsgBox("Export Complete",f"GnuCash transactions have been exported to:\n{output_file}",0)
