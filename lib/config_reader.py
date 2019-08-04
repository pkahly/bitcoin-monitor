import json
import os


CONFIG_FILE = 'config.json'

   
class Config:
   def __init__(self):
      self.enable_emails = False
      self.server = ""
      self.port = ""
      self.bot_email = ""
      self.bot_password = ""
      self.human_email = ""

      self.bitcoind_user = "alerterbot"
      self.bitcoind_pass = "DO_NOT_USE_76cf8e3a30fb29b4131a8babb"
      self.use_testnet = False
      self.use_regtest = False
      
      self.minutes_to_sleep = 5
      self.status_frequency_in_hours = 4
      self.historical_price_filename = 'daily_history.csv'
      self.catch_errors = True
      
      self.block_reorg_threshold = 0
      self.minutes_between_blocks_threshold = 90
      self.price_percent_change_threshold = 5
      self.reorg_depth_cap = 5
   

def get_config():
   _write_config_if_missing()
   
   try:
      return _read_config()
   except KeyError as ex:
      raise RuntimeError("Missing Required Config Option. {}".format(ex))

def _write_config_if_missing():
   if not os.path.isfile(CONFIG_FILE):
      config_str = json.dumps(Config().__dict__)
      
      with open(CONFIG_FILE, 'w') as json_file:
         json_file.write(config_str)
      
      print("Created default config.json")


def _read_config():
   with open(CONFIG_FILE) as json_file:
      config_file = json.load(json_file)
      config = Config()
      
      config.enable_emails = config_file["enable_emails"]
      
      if config.enable_emails:
         config.server = config_file["server"]
         config.port = config_file["port"]
         config.bot_email = config_file["bot_email"]
         config.bot_password = config_file["bot_password"]
         config.human_email = config_file["human_email"]

      config.bitcoind_user = config_file["bitcoind_user"]
      config.bitcoind_pass = config_file["bitcoind_pass"]
      
      config.use_testnet = config_file["use_testnet"]
      config.use_regtest = config_file["use_regtest"]
         
      config.minutes_to_sleep = config_file["minutes_to_sleep"]
      config.status_frequency_in_hours = config_file["status_frequency_in_hours"]
      config.historical_price_filename = config_file["historical_price_filename"]
      config.catch_errors = config_file["catch_errors"]

      config.block_reorg_threshold = config_file["block_reorg_threshold"]
      config.minutes_between_blocks_threshold = config_file["minutes_between_blocks_threshold"]
      config.price_percent_change_threshold = config_file["price_percent_change_threshold"]
      config.reorg_depth_cap = config_file["reorg_depth_cap"]
         
      return config
