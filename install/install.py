#!/usr/bin/python3

import sqlite3

connection = sqlite3.connect("bitcoin.db")
cursor = connection.cursor()

sql_command = """
CREATE TABLE historical_prices (
date DATE PRIMARY KEY,
open REAL,
high REAL,
low REAL,
close REAL,
change REAL,
volume INTEGER,
market_cap INTEGER);"""

cursor.execute(sql_command)

sql_command = """
CREATE TABLE block_info (
height INTEGER PRIMARY KEY,
hash TEXT
);"""

cursor.execute(sql_command)

# Commit and Close
connection.commit()
connection.close()
