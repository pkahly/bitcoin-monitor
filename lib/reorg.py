import sqlite3
import json
import subprocess

REORG_DEPTH_CAP = 5


def get_highest_stored_block(cursor):
   cursor.execute("SELECT height FROM block_info ORDER BY height DESC limit 1")
   result = cursor.fetchone()
   
   if result == None:
      return -1
   else:
      return result[0]

def get_current_hash(height):
   hash = subprocess.check_output(['bitcoin-cli','getblockhash', str(height)])
   return hash.decode("utf-8").replace('\n', '') 


def get_stored_hash(cursor, height):
   cursor.execute("SELECT hash FROM block_info where height = {}".format(int(height)))
   return cursor.fetchone()[0]


def get_last_matching_height(cursor, height):
   while height >= 0:
      old_hash = get_stored_hash(cursor, height)
      new_hash = get_current_hash(height)
      
      if old_hash == new_hash:
         return height
         
      height -= 1
      
      
def delete_rows_after(connection, cursor, height):
   cursor.execute("DELETE FROM block_info where height > {}".format(int(height)))
   connection.commit()
   print("Deleted block info after {}".format(height))
   
   
def add_blocks():
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()

   highest_stored_block = get_highest_stored_block(cursor)
   num_blocks = json.loads(subprocess.check_output(['bitcoin-cli','getblockcount']))

   # Check for reorgs
   last_matching_height = get_last_matching_height(cursor, highest_stored_block)
   if (last_matching_height + REORG_DEPTH_CAP) <= highest_stored_block:
      raise RuntimeError("LARGE REORG DETECTED -- last matching block: {}".format(last_matching_height))
   elif last_matching_height != highest_stored_block:
      delete_rows_after(connection, cursor, last_matching_height)


   # Store hashes of new blocks
   for height in reversed(range(last_matching_height + 1, num_blocks + 1)):
      hash = get_current_hash(height)
      
      sql_command = "INSERT INTO block_info (height, hash)\nVALUES ({}, \"{}\");".format(height, hash)
      cursor.execute(sql_command)
      
      if height % 100 == 0:
         connection.commit()


   # Commit and Close
   connection.commit()
   connection.close()
   
   return {"highest_stored_block": highest_stored_block, "num_blocks": num_blocks, "last_matching_height": last_matching_height}
