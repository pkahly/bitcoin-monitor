#!/usr/bin/python3

from collections import deque
from lib import bitcoin_node_api


client = bitcoin_node_api.BitcoinAPIClient()

blocks = set()
coins = 0

max_height = client.get_num_blocks()
height = 0

while height < max_height:
   coinbase_tx = client.get_verbose_block(height)["tx"][0]
   utxo_data = client.get_utxo(coinbase_tx, 0)
   
   if utxo_data != None:
      blocks.add(height)
      coins += utxo_data["value"]
      print("{} {:,.2f}".format(height, coins))
   
   height += 1#!/usr/bin/python3

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
