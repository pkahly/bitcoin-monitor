#!/usr/bin/python3

import sqlite3

connection = sqlite3.connect("bitcoin.db")
cursor = connection.cursor()

"""
# Create historical_prices table
sql_command = \"""
CREATE TABLE historical_prices (
date DATE PRIMARY KEY,
open REAL,
high REAL,
low REAL,
close REAL,
change REAL,
volume INTEGER,
market_cap INTEGER);\"""

cursor.execute(sql_command)


# Create block_info table
sql_command = \"""
CREATE TABLE block_info (
height INTEGER PRIMARY KEY,
hash TEXT
);\"""

cursor.execute(sql_command)
"""

# Create status_info table
sql_command = """
CREATE TABLE status_info (
timestamp INTEGER PRIMARY KEY,
blocks INTEGER,
difficulty REAL,
network_hash_rate REAL,
price REAL);"""

cursor.execute(sql_command)


# Commit and Close
connection.commit()
connection.close()
