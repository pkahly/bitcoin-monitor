import sqlite3
from datetime import datetime, timedelta
import time


def print_blocks():
   _print_table("block_info", "height", "DESC")


def print_price_history():
   _print_table("historical_prices", "date", "ASC")


def print_status_history():
   _print_table("status_info", "timestamp", "DESC")
   

def _print_table(table_name, order_field, asc_or_desc):
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()

   cursor.execute("SELECT * FROM {} ORDER BY {} {}".format(table_name, order_field, asc_or_desc))

   result = cursor.fetchone()
   while result != None:
       print(result)
       result = cursor.fetchone()
       time.sleep(1)

   connection.close()
