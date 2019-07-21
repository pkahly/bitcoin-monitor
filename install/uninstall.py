#!/usr/bin/python3

import sqlite3

connection = sqlite3.connect("bitcoin.db")
cursor = connection.cursor()

cursor.execute("""DROP TABLE historical_prices;""")
cursor.execute("""DROP TABLE block_info;""")
cursor.execute("""DROP TABLE status_info;""")

# Commit and Close
connection.commit()
connection.close()
