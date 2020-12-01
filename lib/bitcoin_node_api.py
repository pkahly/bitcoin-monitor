from bitcoinrpc.authproxy import AuthServiceProxy
from lib import config_reader
import logging

# Had luck running bitcoind with -rpcuser=alerterbot -rpcpassword=DO_NOT_USE_76cf8e3a30fb29b4131a8babb -rpcbind=127.0.0.1:8332 -rpcallowip=127.0.0.1

BITCOIND_ADDRESS_TEMPLATE = "http://{}:{}@127.0.0.1:{}"
MAINNET_PORT = 8332
TESTNET_PORT = 18332
REGTEST_PORT = 18443


class BitcoinAPIClient:

   def __init__(self, config):
      port = MAINNET_PORT
      if config.use_testnet and config.use_regtest:
         raise RuntimeError("Cannot specify both testnet AND regtest")
      elif config.use_testnet:
         port = TESTNET_PORT
      elif config.use_regtest:
         port = REGTEST_PORT

      address = BITCOIND_ADDRESS_TEMPLATE.format(config.bitcoind_user, config.bitcoind_pass, port)

      self.client = AuthServiceProxy(address, timeout=240)

   def get_current_hash(self, height):
      return self.client.getblockhash(height)
      
   def get_num_blocks(self):
      return self.client.getblockcount()
      
   def get_num_headers(self):
      blockchain_info = self.client.getblockchaininfo()
      return blockchain_info["headers"]

   def get_mining_info(self):
      return self.client.getmininginfo()
      
   def get_network_hashrate(self, num_blocks, height=None):
      if height:
         return self.client.getnetworkhashps(num_blocks, height)
      else:
         return self.client.getnetworkhashps(num_blocks)
      
   def get_one_blockstat(self, block_height, stat):
      return self.get_blockstats(block_height, [stat])[stat]
         
   def get_blockstats(self, block_height, stats):
      if block_height < 0:
         raise RuntimeError("Negative block height requested {}".format(block_height))

      return self.client.getblockstats(block_height, stats)
      
   def get_transaction(self, transaction_id):
      raw_tx = self.client.getrawtransaction(transaction_id)
      return self.client.decoderawtransaction(raw_tx)
      
   def get_block_containing_transaction(self, transaction_id):
      raw_tx = self.client.getrawtransaction(transaction_id, True) # verbose
      block_hash = raw_tx["blockhash"]
      return self.client.getblock(block_hash)
      
   def get_block(self, height):
      block_hash = self.client.getblockhash(height)
      return self.client.getblock(block_hash)
      
   def get_utxo(self, tx_id, vout):
      return self.client.gettxout(tx_id, vout)
      
   def get_banned_nodes(self):
      return self.client.listbanned()
      
   def get_softforks(self):
      blockchain_info = self.client.getblockchaininfo()
      return blockchain_info["softforks"]
