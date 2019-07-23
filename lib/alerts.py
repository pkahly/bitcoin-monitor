BLOCK_REORG_THRESHOLD = 0
MINUTES_BETWEEN_BLOCKS_THRESHOLD = 90
PRICE_PERCENT_CHANGE_THRESHOLD = 10

def get_alerts(previous_info, info):
   alerts = []
   
   if info.num_minutes > MINUTES_BETWEEN_BLOCKS_THRESHOLD:
      alerts.append("WARNING: No blocks in {} minutes".format(info.num_minutes))
   
   if info.difficulty_percent_change > 0:
      alerts.append("Difficulty Adjustment Occurred! Old: {} New: {} Change: {:.2f} %".format(previous_info.difficulty, info.difficulty, info.difficulty_percent_change))
      
   if info.reorg_length > BLOCK_REORG_THRESHOLD:
      alerts.append("WARNING: Block Reorg of {} blocks has occurred".format(info.reorg_length))
      
   if previous_info != None and previous_info.price_alert_enabled and abs(info.price_percent_change) > PRICE_PERCENT_CHANGE_THRESHOLD:
      alerts.append("WARNING: Price change of {:.2f} %".format(info.price_percent_change))
      previous_info.price_alert_enabled = False # TODO find a better way of doing this
   
   return alerts
