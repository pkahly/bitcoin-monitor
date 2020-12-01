import sqlite3
from lib import utxo_reader, bitcoin_node_api

SATOSHIS_PER_BITCOIN = 100000000.0 # 100 million
AMOUNT_THRESHOLD = 0.1

def add_old_utxo(block_height_threshold):
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()

   count = 0
   for utxo in utxo_reader.UtxoIterator():
      # Skip newer utxo
      height = int(utxo["height"])   
      if height > block_height_threshold:
         continue
      
      # Skip tiny utxo
      satoshis = int(utxo["amount"])
      bitcoin = round(satoshis / SATOSHIS_PER_BITCOIN, 2)
      if bitcoin < AMOUNT_THRESHOLD:
         continue
         
      # Write to watchlist
      txid = utxo["txid"]
      vout = int(utxo["vout"])
      sql_command = "INSERT INTO watchlist (txid, vout, height, bitcoin)\nVALUES (\"{}\", {}, {}, {});".format(txid, vout, height, bitcoin)
      cursor.execute(sql_command)
      
      count += 1
      
   # Commit and Close
   connection.commit()
   connection.close()
   
   logging.info("Added {} UTXO to Watchlist".format(count))


def check_watchlist(config):
   client = bitcoin_node_api.BitcoinAPIClient(config)
   
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()

   cursor.execute("""SELECT txid, vout, height, bitcoin FROM watchlist;""")   
   
   result = cursor.fetchone()
   count = 0
   spent_utxo = []
   while result != None:
       txid = result[0]
       vout = result[1]
       height = result[2]
       bitcoin = result[3]
       
       current_utxo = client.get_utxo(txid, vout)
       if not current_utxo:
         info = info = {"txid": txid, "vout": vout, "height": height, "bitcoin": bitcoin}
         logging.info(info)
         spent_utxo.append(info)
       
       result = cursor.fetchone()
       count += 1
   
   connection.close()
   logging.info("Checked all {} UTXO from watchlist".format(count))

   return spent_utxo


def remove_from_watchlist(txid, vout):
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()

   cursor.execute("DELETE FROM watchlist WHERE txid = \"{}\" AND vout = {};".format(txid, int(vout)))

   # Commit and Close
   connection.commit()
   connection.close()
   
   
def remove_all_from_watchlist(spent_utxo):
   for utxo in spent_utxo:
      # TODO do this with a single SQL statement
      remove_from_watchlist(utxo["txid"], utxo["vout"])


def clear_watchlist():
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()

   cursor.execute("""DELETE FROM watchlist;""")   

   # Commit and Close
   connection.commit()
   connection.close()
   logging.info("Watchlist cleared successfully")
