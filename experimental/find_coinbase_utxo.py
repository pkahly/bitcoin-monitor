#!/usr/bin/python3

from collections import deque
from lib import bitcoin_node_api


client = bitcoin_node_api.BitcoinAPIClient()

blocks = set()
coins = 0

max_height = client.get_num_blocks()
height = 100000#1

while height < max_height:
   coinbase_tx_id = client.get_block(height)["tx"][0]
   coinbase_tx = client.get_transaction(coinbase_tx_id)
   num_outputs = len(coinbase_tx["vout"])
   
   is_unspent = True
   vout = 0
   value = 0
   
   # Some coinbase transactions have multiple outputs
   while vout < num_outputs:
      utxo_data = client.get_utxo(coinbase_tx_id, 0)
      if utxo_data == None:
         is_unspent = False
         break
      value += utxo_data["value"]
      vout += 1
      
   if is_unspent:
      blocks.add(height)
      coins += value
      print("{} {:,.2f}".format(height, coins))
   
   height += 1

from collections import deque
from lib import bitcoin_node_api


client = bitcoin_node_api.BitcoinAPIClient()

max_height = client.get_num_blocks()
height = 0

while height < max_height:
   coinbase_tx = client.get_verbose_block(height)["tx"][0]
   
   if client.is_unspent(coinbase_tx, 0):
      print(height)
   
   height += 1
