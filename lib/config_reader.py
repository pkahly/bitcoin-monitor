import json


CONFIG_FILE = 'config.json'

   
class Config:
   enable_emails = False
   server = None
   port = None
   bot_email = None
   bot_password = None
   human_email = None
   
   minutes_to_sleep = 5
   status_frequency_in_hours = 4
   historical_price_filename = 'daily_history.csv'
   
   block_reorg_threshold = 0
   minutes_between_blocks_threshold = 90
   price_percent_change_threshold = 5
   reorg_depth_cap = 5
   

def get_config():
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
         
      config.minutes_to_sleep = config_file["minutes_to_sleep"]
      config.status_frequency_in_hours = config_file["status_frequency_in_hours"]
      config.historical_price_filename = config_file["historical_price_filename"]

      config.block_reorg_threshold = config_file["block_reorg_threshold"]
      config.minutes_between_blocks_threshold = config_file["minutes_between_blocks_threshold"]
      config.price_percent_change_threshold = config_file["price_percent_change_threshold"]
      config.reorg_depth_cap = config_file["reorg_depth_cap"]
         
      return config
