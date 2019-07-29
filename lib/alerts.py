from lib import config_reader

def get_alerts(previous_info, info):
   config = config_reader.get_config()
   alerts = []
   
   if info.num_minutes > config.minutes_between_blocks_threshold:
      alerts.append("WARNING: No blocks in {} minutes".format(info.num_minutes))
   
   if info.difficulty_percent_change > 0:
      alerts.append("Difficulty Adjustment Occurred! Old: {} New: {} Change: {:.2f} %".format(previous_info.difficulty, info.difficulty, info.difficulty_percent_change))
      
   if info.reorg_length > config.block_reorg_threshold:
      alerts.append("WARNING: Block Reorg of {} blocks has occurred".format(info.reorg_length))
      
   if previous_info != None and previous_info.price_alert_enabled and abs(info.price_percent_change) > config.price_percent_change_threshold:
      alerts.append("WARNING: Price change of {:.2f} %".format(info.price_percent_change))
      previous_info.price_alert_enabled = False # TODO find a better way of doing this
   
   return alerts
