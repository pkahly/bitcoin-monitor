import sqlite3
import json
from lib import config_reader

SATOSHIS_PER_BITCOIN = 100000000.0 # 100 million

def get_highest_stored_block(cursor):
   cursor.execute("SELECT height FROM block_info ORDER BY height DESC limit 1")
   result = cursor.fetchone()
   
   if result == None:
      return -1
   else:
      return result[0]


def get_max_hashrate(end_height):
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()
   
   cursor.execute("SELECT networkhashps FROM block_info where height <= {} ORDER BY networkhashps DESC limit 1".format(int(end_height)))
   result = cursor.fetchone()
   
   if result == None:
      return -1
   else:
      return result[0]


def get_min_hashrate(start_height, end_height):
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()
   
   cursor.execute("SELECT networkhashps FROM block_info where height >= {} and height <= {} ORDER BY networkhashps ASC limit 1".format(int(start_height), int(end_height)))
   result = cursor.fetchone()
   
   if result == None:
      return -1
   else:
      return result[0]


def get_stored_hash(cursor, height):
   cursor.execute("SELECT hash FROM block_info where height = {}".format(int(height)))
   return cursor.fetchone()[0]


def get_last_matching_height(bitcoin_client, cursor, height):
   while height >= 0:
      old_hash = get_stored_hash(cursor, height)
      new_hash = bitcoin_client.get_current_hash(height)
      
      if old_hash == new_hash:
         return height
         
      height -= 1
   return -1
      
      
def delete_rows_after(connection, cursor, height):
   cursor.execute("DELETE FROM block_info where height > {}".format(int(height)))
   connection.commit()
   print("Deleted block info after {}".format(height))
   
   
def add_blocks(config, bitcoin_client):
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()

   highest_stored_block = get_highest_stored_block(cursor)
   num_blocks = bitcoin_client.get_num_blocks()

   # Check for reorgs
   last_matching_height = get_last_matching_height(bitcoin_client, cursor, highest_stored_block)
   if (last_matching_height + config.reorg_depth_cap) <= highest_stored_block:
      raise RuntimeError("LARGE REORG DETECTED -- last matching block: {}".format(last_matching_height))
   elif last_matching_height != highest_stored_block:
      delete_rows_after(connection, cursor, last_matching_height)


   # Store hashes of new blocks
   start = last_matching_height + 1
   end = num_blocks + 1
   _overwrite_blocks(bitcoin_client, config, connection, cursor, start, end)


   # Commit and Close
   connection.commit()
   connection.close()
   
   return {"highest_stored_block": highest_stored_block, "num_blocks": num_blocks, "last_matching_height": last_matching_height}
   

def _overwrite_blocks(bitcoin_client, config, connection, cursor, start, end):
   stats = ["blockhash", "total_out", "txs"]
   
   for height in reversed(range(start, end)):
      current_stats = bitcoin_client.get_blockstats(height, stats)
      networkhashps = bitcoin_client.get_network_hashrate(config.network_hash_duration, height)
      
      hash = current_stats["blockhash"]
      satoshis = current_stats["total_out"]
      bitcoin = satoshis / SATOSHIS_PER_BITCOIN
      txcount = current_stats["txs"]
      
      sql_command = "INSERT INTO block_info (height, hash, networkhashps, bitcoin, txcount)\nVALUES ({}, \"{}\", {}, {}, {});".format(height, hash, networkhashps, bitcoin, txcount)
      cursor.execute(sql_command)

      if height % 10 == 0:
         print("Adding Block: {}".format(height)) 
         connection.commit()
