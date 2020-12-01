from enum import Enum
from datetime import datetime, timedelta
from lib import config_reader, price_history
import logging

class AlertType(Enum):
   NO_BLOCKS_IN_MINS = 0
   DIFFICULTY_CHANGE = 1
   HASH_RATE = 2
   BLOCK_TIME = 3
   REORG = 4
   PRICE = 5
   BANLIST = 6
   SOFTFORKS = 7

class AlertGenerator:

   def __init__(self, config):
      self.config = config
      self.alert_cooldowns = {}
      self.cooldown_time = timedelta(hours=config.status_frequency_in_hours)
   
   
   def get_alerts(self, previous_info, info):
      # Get alerts that should have a cooldown
      alert_data = self._get_alert_data(previous_info, info)
      alerts = []
      
      # Enforce cooldown
      for key in alert_data:
         alert_str = alert_data[key]
         
         if self._check_cooldown(key):
            alerts.append(alert_str)
         
      # Get non-cooldown enforced alerts (these are especially important if happening a lot)
      if info.reorg_length > self.config.block_reorg_threshold:
         alerts.append("Block Reorg of {} blocks has occurred".format(info.reorg_length))
         
      return alerts
      

   def _check_cooldown(self, key):
      if not key in self.alert_cooldowns:
         self.alert_cooldowns[key]  = datetime.now()
         return True
         
      last_alert = self.alert_cooldowns[key]
      difference = datetime.now() - last_alert
      
      if difference > self.cooldown_time:
         self.alert_cooldowns[key]  = datetime.now()
         return True
      
      return False
   
   
   def _get_alert_data(self, previous_info, info):
      alert_data = {}
      
      if info.num_minutes > self.config.minutes_between_blocks_threshold:
         alert_data[AlertType.NO_BLOCKS_IN_MINS] = "No blocks in {} minutes".format(info.num_minutes)
      
      if info.difficulty_percent_change > 0:
         alert_data[AlertType.DIFFICULTY_CHANGE] = "Difficulty Adjustment Occurred! Old: {} New: {} Change: {:.2f} %".format(previous_info.difficulty, info.difficulty, info.difficulty_percent_change)
         
      if hasattr(info, 'max_hash_rate') and info.max_hash_rate < info.network_hash_rate:
         hashrate_str = price_history.to_human_readable_large_number(info.network_hash_rate, price_history.HASHES_WORD_DICT)
         max_hashrate_str = price_history.to_human_readable_large_number(info.max_hash_rate, price_history.HASHES_WORD_DICT)
         alert_data[AlertType.HASH_RATE] = 'Above Maximum Hash Rate: {} > {}'.format(hashrate_str, max_hashrate_str)
         
      if hasattr(info, 'min_hash_rate') and info.min_hash_rate > info.network_hash_rate:
         hashrate_str = price_history.to_human_readable_large_number(info.network_hash_rate, price_history.HASHES_WORD_DICT)
         min_hashrate_str = price_history.to_human_readable_large_number(info.min_hash_rate, price_history.HASHES_WORD_DICT)
         alert_data[AlertType.HASH_RATE] = 'Below Local Minimum Hash Rate: {} < {}'.format(hashrate_str, min_hashrate_str)
         
      if abs(info.daily_avg - 10) > 2: # TODO make threshold a configuration option
         alert_data[AlertType.BLOCK_TIME] = "Unusual Block Time: {:.2f} min".format(info.daily_avg)
         
      if abs(info.price_percent_change) > self.config.price_percent_change_threshold:
         alert_data[AlertType.PRICE] = "Price change of {:.2f} %".format(info.price_percent_change)
         
      if previous_info.banlist_hash != info.banlist_hash:
         alert_data[AlertType.BANLIST] = "Banlist has changed: {}".format(info.banlist)
         
      if previous_info.softforks_hash != info.softforks_hash:
         alert_data[AlertType.SOFTFORKS] = "Softforks have changed: {}".format(info.softforks)
      
      return alert_data
