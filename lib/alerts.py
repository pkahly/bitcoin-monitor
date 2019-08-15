from lib import config_reader, price_history

def get_alerts(previous_info, info):
   config = config_reader.get_config()
   alerts = []
   
   if info.num_minutes > config.minutes_between_blocks_threshold:
      alerts.append("WARNING: No blocks in {} minutes".format(info.num_minutes))
   
   if info.difficulty_percent_change > 0:
      alerts.append("Difficulty Adjustment Occurred! Old: {} New: {} Change: {:.2f} %".format(previous_info.difficulty, info.difficulty, info.difficulty_percent_change))
      
   if info.max_hash_rate < info.network_hash_rate:
      hashrate_str = price_history.to_human_readable_large_number(info.network_hash_rate, price_history.HASHES_WORD_DICT)
      max_hashrate_str = price_history.to_human_readable_large_number(info.max_hash_rate, price_history.HASHES_WORD_DICT)
      alerts.append('WARNING: Above Maximum Hash Rate: {} > {}'.format(hashrate_str, max_hashrate_str))
      
   if info.min_hash_rate > info.network_hash_rate:
      hashrate_str = price_history.to_human_readable_large_number(info.network_hash_rate, price_history.HASHES_WORD_DICT)
      min_hashrate_str = price_history.to_human_readable_large_number(info.min_hash_rate, price_history.HASHES_WORD_DICT)
      alerts.append('WARNING: Below Local Minimum Hash Rate: {} < {}'.format(hashrate_str, min_hashrate_str))
      
   if abs(info.daily_avg - 10) > 1:
      alerts.append("WARNING: Unusual Block Time: {} min".format(info.daily_avg))
      
   if info.reorg_length > config.block_reorg_threshold:
      alerts.append("WARNING: Block Reorg of {} blocks has occurred".format(info.reorg_length))
      
   if abs(info.price_percent_change) > config.price_percent_change_threshold:
      alerts.append("WARNING: Price change of {:.2f} %".format(info.price_percent_change))
   
   return alerts
