#!/usr/bin/python3

import time
from lib import utxo_reader, watchlist

SATOSHIS_PER_BITCOIN = 100000000.0 # 100 million
BLOCK_HEIGHT_THRESHOLD = 100000

count = 0
for utxo in utxo_reader.UtxoIterator():
   # Print progress
   try:
      if int(utxo["count"]) % 1000000 == 0:
         print(utxo["count"])
   except ValueError:
      break

   # Skip newer utxo
   height = int(utxo["height"])   
   if height > BLOCK_HEIGHT_THRESHOLD:
      continue
   
   # Skip tiny utxo
   satoshis = int(utxo["amount"])
   bitcoin = round(satoshis / SATOSHIS_PER_BITCOIN, 3)
   if bitcoin == 0:
      continue
      
   count += 1
   
print("Old UTXO Found: {}".format(count))
