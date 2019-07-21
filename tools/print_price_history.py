#!/usr/bin/python3

import sqlite3
from datetime import datetime, timedelta
import time

connection = sqlite3.connect("bitcoin.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM historical_prices ORDER BY date ASC")

result = cursor.fetchone()
while result != None:
    print(result)
    result = cursor.fetchone()
    time.sleep(1)

connection.close()
