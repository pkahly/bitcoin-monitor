#!/usr/bin/python3

from statistics import mean
from lib import bitcoin_node_api, config_reader

START_BLOCK = 591456
END_BLOCK = 591556
NUM_RESULTS = 10

config = config_reader.load_config()
client = bitcoin_node_api.BitcoinAPIClient(config)

# Format: {"txid": txid, "value": value}
transactions = []

# Loop over all blocks in the range
height = START_BLOCK

while height <= END_BLOCK:
   current_block = client.get_block(height)
   print("block: {}".format(height))
   
   # Loop over all transactions in the block   
   tx_list = current_block["tx"]
   for tx_id in tx_list:
      tx = client.get_transaction(tx_id)
      
      # Get value of the transaction
      tx_value = 0
      for vout in tx["vout"]:
         tx_value += vout["value"]
      tx_value = float(round(tx_value, 2))

      # Add to transaction list
      if tx_value > 0:
         transactions.append({"txid": tx_id, "value": tx_value})

   # Sort transactions DESC
   transactions.sort(key=lambda tx: tx["value"], reverse=True)
   
   # Only keep first N
   transactions = transactions[0:NUM_RESULTS]
   
   print(transactions)
   print()
   print()   
   
   height += 1
   
# Print results
for tx in transactions:
   print("{}  {:>10,}".format(tx["txid"], tx["value"]))
