#!/usr/bin/python3

from lib import utxo_reader

SATOSHIS_PER_BITCOIN = 100000000.0 # 100 million

blocks = set()
total_coins = 0

for utxo in utxo_reader.UtxoIterator():
   # Print progress
   try:
      if int(utxo["count"]) % 1000000 == 0:
         print(utxo["count"])
   except ValueError:
      break
   
   # Skip non-coinbase utxo
   if utxo["coinbase"] == "0":
      continue
   
   height = int(utxo["height"])
   satoshis = int(utxo["amount"])
   bitcoin = round(satoshis / SATOSHIS_PER_BITCOIN, 3)
   
   # Skip tiny utxo
   if bitcoin == 0:
      continue
   
   blocks.add(height)
   total_coins += bitcoin
   

print(blocks)   
print(total_coins)
