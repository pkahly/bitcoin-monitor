#!/usr/bin/python3

import sqlite3
import math
from datetime import datetime
from lib import price_history

FILENAME = '../daily_history.csv'

connection = sqlite3.connect("../bitcoin.db")
cursor = connection.cursor()

with open(FILENAME, 'r') as file:
   for line in reversed(list(file)):
      line_split = line.rstrip().split(',')

      date = datetime.strptime(line_split[0], "%b%d%Y").strftime("%Y-%m-%d")

      open = float(line_split[1])
      high = float(line_split[2])
      low = float(line_split[3])
      close = float(line_split[4])
      
      volume = 0
      if line_split[5] != "-":
         volume = int(line_split[5])
   
      market_cap = 0
      if line_split[6] != "-":
         market_cap = int(line_split[6])

      change = round(price_history.percent_change(open, close), 2)

      sql_command = "INSERT INTO historical_prices (date, open, high, low, close, change, volume, market_cap)\nVALUES (\"{}\", {}, {}, {}, {}, {}, {}, {});".format(date, open, high, low, close, change, volume, market_cap)
      cursor.execute(sql_command)

# Commit and Close
connection.commit()
connection.close()
