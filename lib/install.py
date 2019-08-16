import sqlite3
from datetime import datetime
from lib import reorg, price_history, config_reader, bitcoin_node_api


def install():
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()

   # Create historical_prices table
   sql_command = """
   CREATE TABLE historical_prices (
   date DATE PRIMARY KEY,
   open REAL NOT NULL,
   high REAL NOT NULL,
   low REAL NOT NULL,
   close REAL NOT NULL,
   change REAL NOT NULL,
   volume INTEGER,
   market_cap INTEGER);"""

   cursor.execute(sql_command)


   # Create block_info table
   sql_command = """
   CREATE TABLE block_info (
   height INTEGER PRIMARY KEY,
   hash TEXT NOT NULL,
   networkhashps REAL NOT NULL
   );"""

   cursor.execute(sql_command)


   # Create status_info table
   sql_command = """
   CREATE TABLE status_info (
   timestamp INTEGER PRIMARY KEY,
   blocks INTEGER NOT NULL,
   difficulty REAL NOT NULL,
   network_hash_rate REAL NOT NULL,
   price REAL NOT NULL);"""

   cursor.execute(sql_command)


   # Create watchlist table
   sql_command = """
   CREATE TABLE watchlist (
   txid TEXT NOT NULL,
   vout INTEGER NOT NULL,
   UNIQUE (txid, vout));"""

   cursor.execute(sql_command)

   
   # Commit and Close
   connection.commit()
   connection.close()
   print("Install completed successfully")


def add_blocks():
   client = bitcoin_node_api.BitcoinAPIClient()
   reorg_info = reorg.add_blocks(client)

   highest_stored_block = reorg_info["highest_stored_block"]
   num_blocks = reorg_info["num_blocks"]
   last_matching_height = reorg_info["last_matching_height"]

   print("Highest Stored Block: {}".format(highest_stored_block))
   print("Newest Block: {}".format(num_blocks))

   if last_matching_height != highest_stored_block:
      print("WARNING! Reorg occurred after block {}".format(last_matching_height))

   print("Added {} blocks to database".format(num_blocks - last_matching_height))



def import_historical_prices():
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()

   config = config_reader.get_config()
   with open(config.historical_price_filename, 'r') as file:
      lines = list(file)
      num_lines = len(lines)
      for line in reversed(lines):
         line_split = line.rstrip().split(',')

         date = datetime.strptime(line_split[0], "%b%d%Y").strftime("%Y-%m-%d")

         open_price = float(line_split[1])
         high = float(line_split[2])
         low = float(line_split[3])
         close = float(line_split[4])
         
         volume = 0
         if line_split[5] != "-":
            volume = int(line_split[5])
      
         market_cap = 0
         if line_split[6] != "-":
            market_cap = int(line_split[6])

         change = round(price_history.percent_change(open_price, close), 2)

         sql_command = "INSERT INTO historical_prices (date, open, high, low, close, change, volume, market_cap)\nVALUES (\"{}\", {}, {}, {}, {}, {}, {}, {});".format(date, open_price, high, low, close, change, volume, market_cap)
         cursor.execute(sql_command)

   # Commit and Close
   connection.commit()
   connection.close()
   print("Added {} historical price points to database".format(num_lines))
   
   
def uninstall():
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()

   cursor.execute("""DROP TABLE historical_prices;""")
   cursor.execute("""DROP TABLE block_info;""")
   cursor.execute("""DROP TABLE status_info;""")
   cursor.execute("""DROP TABLE watchlist;""")   

   # Commit and Close
   connection.commit()
   connection.close()
   print("Uninstall completed successfully")
