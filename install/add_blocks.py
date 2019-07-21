#!/usr/bin/python3

import sqlite3
import math
import json
import subprocess
from lib import reorg

reorg_info = reorg.add_blocks()

highest_stored_block = reorg_info["highest_stored_block"]
num_blocks = reorg_info["num_blocks"]
last_matching_height = reorg_info["last_matching_height"]

print("Highest Stored Block: {}".format(highest_stored_block))
print("Newest Block: {}".format(num_blocks))

if last_matching_height != highest_stored_block:
   print("WARNING! Reorg occurred after block {}".format(last_matching_height))

print("Added {} blocks to database".format(num_blocks - last_matching_height))
