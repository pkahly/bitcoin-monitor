import sqlite3
from datetime import datetime
from lib import reorg, price_history


HISTORICAL_PRICE_FILENAME = 'daily_history.csv'


def install():
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()

   # Create historical_prices table
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


   # Create block_info table
   sql_command = """
   CREATE TABLE block_info (
   height INTEGER PRIMARY KEY,
   hash TEXT
   );"""

   cursor.execute(sql_command)

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


def add_blocks():
   reorg_info = reorg.add_blocks()

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

   with open(HISTORICAL_PRICE_FILENAME, 'r') as file:
      for line in reversed(list(file)):
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
   
   
def uninstall():
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()

   cursor.execute("""DROP TABLE historical_prices;""")
   cursor.execute("""DROP TABLE block_info;""")
   cursor.execute("""DROP TABLE status_info;""")

   # Commit and Close
   connection.commit()
   connection.close()
