#!/usr/bin/python3

import time

# Reads UTXO info from a CSV file
# This file can be generated using a variety of tools
# One such tool: https://github.com/in3rsha/bitcoin-utxo-dump
# Use command 'utxodump  -f count,txid,vout,height,coinbase,amount,script,type,address'

# Reads UTXO info from this file:
UTXO_FILE = "utxo.csv"

with open(UTXO_FILE, 'r') as file:
   while file:
      line = file.readline().replace('\n', '')
      line_split = line.split(',')
      print(line_split)
      time.sleep(1)
