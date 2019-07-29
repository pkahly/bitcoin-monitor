import json


CONFIG_FILE = 'config.json'


class Config:
   enable_emails = False
   server = None
   port = None
   bot_email = None
   bot_password = None
   human_email = None
   

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
         
      return config
