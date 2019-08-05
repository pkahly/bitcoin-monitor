import sqlite3
from lib import price_history


def get_status(previous_info, info):
   statuses = []

   statuses.append("Blocks: {:,} ( + {} )".format(info.blocks, info.new_blocks))
   statuses.append("Last Block Time: {}".format(info.last_block_time.strftime("%m-%d %I:%M %p")))
   statuses.append("Minutes Since Last Block: {}".format(info.num_minutes))
   
   statuses.append("")
   
   statuses.append("Difficulty: {}".format(info.difficulty))
   statuses.append("Blocks until next difficulty adjustment: {:,}".format(info.blocks % 2016))
   
   statuses.append("")
   
   statuses.append("Network Hash Rate: {} ( {:.2f} % )".format(info.network_hash_rate, info.hash_rate_percent_change))
   
   statuses.append("")
   
   statuses.append("Average time between blocks")
   statuses.append("Last day: {:.2f} min".format(info.daily_avg))
   statuses.append("Last week: {:.2f} min".format(info.weekly_avg))
   statuses.append("Last month: {:.2f} min".format(info.monthly_avg))
   
   statuses.append("")
   
   statuses.append("Total Coins Mined: {:,.0f} ( {:.2f} % )".format(info.total_coins, info.coins_mined_percent))
   statuses.append("Remaining Coins: {:,.0f}".format(info.remaining_coins))   
   statuses.append("Current Reward: {}".format(info.reward))
   statuses.append("Blocks Until Next Halving: {:,.0f} ( ~{:,.0f} days )".format(info.blocks_till_halving, info.days_till_halving))

   statuses.append("")
   
   statuses.append("Price: ${:,.2f} ( {:.2f} % )".format(info.price, info.price_percent_change))
   market_cap_str = price_history.to_human_readable_large_number(info.total_coins * info.price)
   statuses.append("Market Cap: ${}".format(market_cap_str))

   statuses.append("")
   
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()
   
   statuses.append("Historical Prices:")
   
   for years_ago in range(1, 6):
      history_info = price_history.get_historical_price(cursor, years_ago)
      if history_info == None:
         continue
      
      old_date_str = history_info[0]
      old_price = history_info[1]

      old_price_str = "${:,.2f}".format(old_price)
      price_percent_change = price_history.percent_change(old_price, info.price)
      
      statuses.append("{} : {:>10} {:>10.2f} %".format(old_date_str, old_price_str, price_percent_change))

   connection.close()
   
   return "\n".join(statuses)   
