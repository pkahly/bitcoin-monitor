import sqlite3
from lib import utxo_reader

SATOSHIS_PER_BITCOIN = 100000000.0 # 100 million

def add_old_utxo(block_height_threshold):
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()

   count = 0
   for utxo in utxo_reader.UtxoIterator():
      # Print progress
      try:
         if int(utxo["count"]) % 1000000 == 0:
            print("Processed {} UTXO".format(utxo["count"]))
      except ValueError:
         break

      # Skip newer utxo
      height = int(utxo["height"])   
      if height > block_height_threshold:
         continue
      
      # Skip tiny utxo
      satoshis = int(utxo["amount"])
      bitcoin = round(satoshis / SATOSHIS_PER_BITCOIN, 3)
      if bitcoin == 0:
         continue
         
      # Write to watchlist
      txid = utxo["txid"]
      vout = int(utxo["vout"])
      sql_command = "INSERT INTO watchlist (txid, vout)\nVALUES (\"{}\", {});".format(txid, vout)
      cursor.execute(sql_command)
      
      count += 1
      
   # Commit and Close
   connection.commit()
   connection.close()
   
   print("Added {} UTXO to Watchlist".format(count))
   
   
def clear_watchlist():
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()

   cursor.execute("""DELETE FROM watchlist;""")   

   # Commit and Close
   connection.commit()
   connection.close()
   print("Watchlist cleared successfully")
