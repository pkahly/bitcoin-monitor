#!/usr/bin/python3

from collections import deque
from lib import bitcoin_node_api

PIZZA_TRANSACTION = "a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d"


client = bitcoin_node_api.BitcoinAPIClient()

tx_id = input("Enter transaction ID (or blank to use Bitcoin pizza) > ")
if not tx_id:
   tx_id = PIZZA_TRANSACTION
   
depth = 0
tx_queue = deque([(depth, tx_id)])

previous_depth = -1
utxo_set = set()
visited = set()

while tx_queue:
   depth, tx_id = tx_queue.popleft()
   
   if previous_depth != depth:
      previous_depth = depth
      print()
      print("Depth: {}".format(depth))
      print("Size of queue: {}".format(len(tx_queue) + 1))
   
   tx = client.get_transaction(tx_id)
   output_list = tx["vout"]
   
   # Add inputs to queue
   for vout in range(0, len(output_list)):
      utxo = client.get_utxo(tx_id, vout)
      
      if utxo == None:
         print(output_list[vout])
         
         # BitcoinCore does not appear to have a way of determining what transactions use this output as an input
         # TODO implement an index or use another tool
         raise RuntimeError("Not Implemented")
         
         if not childtx_id in visited:
            visited.add(childtx_id)
            tx_queue.append((depth + 1, childtx_id))
      else:
         utxo_set.add(utxo)
         
   
print()
print("UTXO descended from this transaction:")
print(utxo_set)
