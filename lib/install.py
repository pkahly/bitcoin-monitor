import sqlite3
from datetime import datetime
from lib import reorg, price_history, bitcoin_node_api


def install():
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()

   # Create historical_prices table
   sql_command = """
   CREATE TABLE historical_prices (
   timestamp INTEGER PRIMARY KEY,
   date DATE NOT NULL UNIQUE,
   open REAL NOT NULL,
   high REAL NOT NULL,
   low REAL NOT NULL,
   close REAL NOT NULL
   );"""

   cursor.execute(sql_command)


   # Create block_info table
   sql_command = """
   CREATE TABLE block_info (
   height INTEGER PRIMARY KEY,
   hash TEXT NOT NULL,
   networkhashps REAL NOT NULL,
   bitcoin REAL NOT NULL,
   txcount INTEGER NOT NULL
   );"""

   cursor.execute(sql_command)


   # Create status_info table
   sql_command = """
   CREATE TABLE status_info (
   timestamp INTEGER PRIMARY KEY,
   blocks INTEGER NOT NULL,
   difficulty REAL NOT NULL,
   network_hash_rate REAL NOT NULL,
   price REAL NOT NULL,
   banlist_hash TEXT NOT NULL,
   softforks_hash TEXT NOT NULL
   );"""

   cursor.execute(sql_command)


   # Create watchlist table
   sql_command = """
   CREATE TABLE watchlist (
   txid TEXT NOT NULL,
   vout INTEGER NOT NULL,
   height INTEGER NOT NULL,
   bitcoin REAL NOT NULL,
   UNIQUE (txid, vout)
   );"""

   cursor.execute(sql_command)

   
   # Commit and Close
   connection.commit()
   connection.close()
   print("Install completed successfully")


def add_blocks(config):
   client = bitcoin_node_api.BitcoinAPIClient(config)
   reorg_info = reorg.add_blocks(config, client)

   highest_stored_block = reorg_info["highest_stored_block"]
   num_blocks = reorg_info["num_blocks"]
   last_matching_height = reorg_info["last_matching_height"]

   print("Highest Stored Block: {}".format(highest_stored_block))
   print("Newest Block: {}".format(num_blocks))

   if last_matching_height != highest_stored_block:
      print("WARNING! Reorg occurred after block {}".format(last_matching_height))

   print("Added {} blocks to database".format(num_blocks - last_matching_height))



def import_historical_prices(filename):
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()

   with open(filename, 'r') as file:
      # Remove heading
      heading = file.readline().rstrip()
      print("Ignored CSV Heading: {}".format(heading))
      
      # Autodetect date format
      line = _peek_line(file)
      date_str = line[0:line.index(',')]
      date_format = _get_date_format(date_str)
      print("Autodetected Date Format as: {}".format(date_format))
      
      # Import
      num_lines = 0
      for line in file:
         line = line.rstrip()
         line_split = line.split(',')

         try:
            date = datetime.strptime(line_split[0], date_format)
            date_str = date.strftime("%Y-%m-%d")
            timestamp = datetime.timestamp(date)

            open_price = float(line_split[1])
            high = float(line_split[2])
            low = float(line_split[3])
            close = float(line_split[4])
         except:
            print("Skipping Invalid Line: {}".format(line))

         try:
            sql_command = "INSERT INTO historical_prices (date, timestamp, open, high, low, close)\nVALUES (\"{}\", {}, {}, {}, {}, {});".format(date_str, timestamp, open_price, high, low, close)
            cursor.execute(sql_command)
            num_lines += 1
         except sqlite3.IntegrityError:
            # Skip duplicates
            continue

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
   

def _get_date_format(date_str):
    date_patterns = ["%d-%m-%Y", "%Y-%m-%d", "%b%d%Y"]

    for pattern in date_patterns:
        try:
            datetime.strptime(date_str, pattern)
            return pattern
        except:
            continue

    raise RuntimeError("Date is not in a supported format: '{}'. Allowed Formats: {}".format(date_str, ", ".join(date_patterns)))


def _peek_line(file):
   pos = file.tell()
   line = file.readline()
   file.seek(pos)
   return line
