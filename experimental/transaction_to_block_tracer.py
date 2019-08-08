#!/usr/bin/python3

from collections import deque
from lib import bitcoin_node_api

PIZZA_TRANSACTION = "a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d"


def get_blocks_str(original_blocks):
   return ", ".join(sorted(original_blocks))


client = bitcoin_node_api.BitcoinAPIClient()

tx_id = input("Enter transaction ID (or blank to use Bitcoin pizza) > ")
if not tx_id:
   tx_id = PIZZA_TRANSACTION
   
depth = 0
tx_queue = deque([(depth, tx_id)])

original_blocks = set()
just_found_blocks = set()
previous_depth = -1

visited = set()

while tx_queue:
   depth, tx_id = tx_queue.popleft()
   
   tx = client.get_transaction(tx_id)
   input_list = tx["vin"]
   
   if previous_depth != depth:
      previous_depth = depth
      print()
      print("Depth: {}".format(depth))
      print("Size of queue: {}".format(len(tx_queue) + 1))
      print("Found blocks: {}".format(get_blocks_str(just_found_blocks)))
      just_found_blocks = set()
   
   if "coinbase" in input_list[0]:
      # This is a coinbase transaction
      block = client.get_block_containing_transaction(tx_id)
      height = str(block["height"])
      original_blocks.add(height)
      just_found_blocks.add(height)
   else:
      # Add inputs to queue
      for tx_input in input_list:
         childtx_id = tx_input["txid"]
         
         if not childtx_id in visited:
            visited.add(childtx_id)
            tx_queue.append((depth + 1, childtx_id))
         
   
print()
print("Blocks the coins in this transaction were mined from:")
print(get_blocks_str(original_blocks))
