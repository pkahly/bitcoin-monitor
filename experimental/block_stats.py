#!/usr/bin/python3

import time
from statistics import mean
from lib import bitcoin_node_api, config_reader

config = config_reader.load_config()
client = bitcoin_node_api.BitcoinAPIClient(config)

STATS = ["avgfeerate", "mediantxsize", "swtxs", "total_weight", "txs", "utxo_increase"]

max_height = client.get_num_blocks()
height = 0
while height <= max_height:
   current_stats = client.get_blockstats(height, STATS)
   
   print(height)
   print(current_stats)
   
   height += 1
   time.sleep(1)
