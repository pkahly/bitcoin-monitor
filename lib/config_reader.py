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
      
      self.status_frequency_in_hours = 6
      self.catch_errors = True
      self.daily_summary_hour = 8
      
      self.block_reorg_threshold = 0
      self.minutes_between_blocks_threshold = 90
      self.price_percent_change_threshold = 5
      self.reorg_depth_cap = 5
      
      self.network_hash_duration = 144
      self.local_min_hashrate_blocks = 10000
   

def load_config():
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
      
      config.enable_emails = _get_config_param_or_use_default(config, config_file, "enable_emails")
      
      if config.enable_emails:
         config.server = _get_config_param_or_use_default(config, config_file, "server")
         config.port = _get_config_param_or_use_default(config, config_file, "port")
         config.bot_email = _get_config_param_or_use_default(config, config_file, "bot_email")
         config.bot_password = _get_config_param_or_use_default(config, config_file, "bot_password")
         config.human_email = _get_config_param_or_use_default(config, config_file, "human_email")

      config.bitcoind_user = _get_config_param_or_use_default(config, config_file, "bitcoind_user")
      config.bitcoind_pass = _get_config_param_or_use_default(config, config_file, "bitcoind_pass")
      
      config.use_testnet = _get_config_param_or_use_default(config, config_file, "use_testnet")
      config.use_regtest = _get_config_param_or_use_default(config, config_file, "use_regtest")
         
      config.status_frequency_in_hours = _get_config_param_or_use_default(config, config_file, "status_frequency_in_hours")
      config.catch_errors = _get_config_param_or_use_default(config, config_file, "catch_errors")
      config.daily_summary_hour = _get_config_param_or_use_default(config, config_file, "daily_summary_hour")

      config.block_reorg_threshold = _get_config_param_or_use_default(config, config_file, "block_reorg_threshold")
      config.minutes_between_blocks_threshold = _get_config_param_or_use_default(config, config_file, "minutes_between_blocks_threshold")
      config.price_percent_change_threshold = _get_config_param_or_use_default(config, config_file, "price_percent_change_threshold")
      config.reorg_depth_cap = _get_config_param_or_use_default(config, config_file, "reorg_depth_cap")
      
      config.network_hash_duration = _get_config_param_or_use_default(config, config_file, "network_hash_duration")
      config.local_min_hashrate_blocks = _get_config_param_or_use_default(config, config_file, "local_min_hashrate_blocks")
         
      return config
      
      
def _get_config_param_or_use_default(config, config_file, param):
   if param in config_file:
      return config_file [param]
   else:
      return getattr(config, param)
