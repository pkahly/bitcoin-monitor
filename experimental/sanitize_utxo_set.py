#!/usr/bin/python3

from lib import utxo_reader

# Writes a new CSV file containing some of the info from utxo.csv
# This allows experimenting with different settings for the watchlist
# without having to loop over a very large file every time
# Filters out UTXO that are too small or are beyond a certain block height
# Also only writes out fields that will likely be used by other scripts

VALUE_THRESHOLD = 1000000 # 1/100 of a bitcoin
HEIGHT_THRESHOLD = 300000

NEW_FILE = "new_utxo.csv"
FIELDS_TO_SAVE = ["txid", "vout", "height", "coinbase", "amount"]

with open(NEW_FILE, 'w') as file:
   # Write header
   header = ",".join(FIELDS_TO_SAVE)
   file.write(header + "\n")
   
   # Find and save utxo that match criteria
   num_written = 0
   for utxo in utxo_reader.UtxoIterator():
      # Print progress
      try:
         if int(utxo["count"]) % 1000000 == 0:
            print(utxo["count"])
      except ValueError:
         # EOF
         break
      
      # Skip utxo after HEIGHT
      height = int(utxo["height"])
      if height > HEIGHT_THRESHOLD:
         continue
      
      # Skip tiny utxo
      satoshis = int(utxo["amount"])
      if satoshis < VALUE_THRESHOLD:
         continue
      
      # Collect info to store
      info = []
      for key in FIELDS_TO_SAVE:
         info.append(utxo[key])
      line = ",".join(info)
      
      # Write
      file.write(line + "\n")
      num_written += 1
   
print("Wrote {} records to {}".format(num_written, NEW_FILE))
