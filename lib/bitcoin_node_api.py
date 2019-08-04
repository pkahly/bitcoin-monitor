from bitcoinrpc.authproxy import AuthServiceProxy
from lib import config_reader

BITCOIND_ADDRESS_TEMPLATE = "http://{}:{}@127.0.0.1:{}"
MAINNET_PORT = 8332
TESTNET_PORT = 18332
REGTEST_PORT = 18443

config = config_reader.get_config()
port = MAINNET_PORT

address = BITCOIND_ADDRESS_TEMPLATE.format(config.bitcoind_user, config.bitcoind_pass, port)
client = AuthServiceProxy(address)


def get_current_hash(height):
   return client.getblockhash(height)
   

def get_num_blocks():
   return client.getblockcount()
   
   
def get_num_headers():
   blockchain_info = client.getblockchaininfo()
   return blockchain_info["headers"]


def get_mining_info():
   return client.getmininginfo()
   
   
def get_blockstats(block_height, stat):
   if block_height < 0:
      raise RuntimeError("Negative block height requested {}".format(block_height))

   block_stats = client.getblockstats(block_height, [stat])
   return block_stats[stat]
