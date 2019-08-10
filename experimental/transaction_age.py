#!/usr/bin/python3

import time
from statistics import mean
from lib import bitcoin_node_api


client = bitcoin_node_api.BitcoinAPIClient()

max_height = client.get_num_blocks()
height = 1

while height <= max_height:
   current_block = client.get_block(height)
   current_block_time = current_block["mediantime"]
   tx_list = current_block["tx"]
   
   print()
   print("block: {}\ntransactions: {}".format(height, len(tx_list)))
   
   tx_ages = []
   for tx_id in tx_list:
      tx = client.get_transaction(tx_id)
      input_list = tx["vin"]
      
      if "coinbase" in input_list[0]:
         continue
      
      input_ages = []
      for tx_input in input_list:
         previous_tx_id = tx_input["txid"]
         prev_block = client.get_block_containing_transaction(previous_tx_id)
         prev_block_time = prev_block["mediantime"]
         input_ages.append(current_block_time - prev_block_time)
         
      tx_ages.append(mean(input_ages))

   if tx_ages:
      average_age = mean(tx_ages)
   else:
      average_age = 0
   
   print("Average TX Age: {:.0f}".format(average_age))
   height += 1
