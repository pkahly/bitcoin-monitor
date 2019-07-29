import subprocess
import json


def get_current_hash(height):
   hash = subprocess.check_output(['bitcoin-cli','getblockhash', str(height)])
   return hash.decode("utf-8").replace('\n', '') 
   

def get_num_blocks():
   return json.loads(subprocess.check_output(['bitcoin-cli','getblockcount']))


def get_mining_info():
   return json.loads(subprocess.check_output(['bitcoin-cli','getmininginfo']))
   
   
def get_blockstats(block_height, stat):
   block_stats = json.loads(subprocess.check_output(['bitcoin-cli','getblockstats',str(block_height),json.dumps([stat])]))
   return block_stats[stat]
