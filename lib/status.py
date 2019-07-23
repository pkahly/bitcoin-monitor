import sqlite3
import subprocess
import requests
import os
from datetime import datetime, timedelta
from lib import reorg, price_history


BLOCK_REORG_THRESHOLD = 0
MINUTES_BETWEEN_BLOCKS_THRESHOLD = 90
PRICE_PERCENT_CHANGE_THRESHOLD = 10

BLOCKS_PER_DAY = 144.0 # 6 per hour * 24 hours per day
BLOCKS_PER_WEEK = 1008.0 # 144 * 7
BLOCKS_PER_MONTH = 4032.0 # 1008 * 4


def write_block_stats(statuses, alerts, previous_info, info):
   statuses.append("Blocks: {:,} ( + {} )".format(info.blocks, info.new_blocks))
   statuses.append("Last Block Time: {}".format(info.last_block_time.strftime("%m-%d %I:%M %p")))
   statuses.append("Minutes Since Last Block: {}".format(info.num_minutes))

   if info.num_minutes > MINUTES_BETWEEN_BLOCKS_THRESHOLD:
      alerts.append("WARNING: No blocks in {} minutes".format(info.num_minutes))
      
      
def write_difficulty_stats(statuses, alerts, previous_info, info):
   statuses.append("Difficulty: {}".format(info.difficulty))
   statuses.append("Network Hash Rate: {} ( {:.2f} % )".format(info.network_hash_rate, info.hash_rate_percent_change))
   
   if info.difficulty_percent_change > 0:
      alerts.append("Difficulty Adjustment Occurred! Old: {} New: {} Change: {:.2f} %".format(previous_info.difficulty, info.difficulty, info.difficulty_percent_change))
      
   statuses.append("Average time between blocks in last day: {:.2f} min".format(info.daily_avg))
   statuses.append("Average time between blocks in last week: {:.2f} min".format(info.weekly_avg))
   statuses.append("Average time between blocks in last month: {:.2f} min".format(info.monthly_avg))

   
def write_reorg_stats(statuses, alerts, previous_info, info):
   if info.reorg_length > BLOCK_REORG_THRESHOLD:
      alerts.append("WARNING: Block Reorg of {} blocks has occurred".format(info.reorg_length))


def write_halving_stats(statuses, alerts, previous_info, info):  
   statuses.append("Total Coins Mined: {:,.0f}".format(info.total_coins))
   statuses.append("Current Reward: {}".format(info.reward))
   statuses.append("Blocks Until Next Halving: {:,.0f} ( ~{:,.0f} days )".format(info.blocks_till_halving, info.days_till_halving))


def write_price_stats(statuses, alerts, previous_info, info):   
   price_percent_change = 0
   if previous_info != None:
       price_percent_change = price_history.percent_change(previous_info.price, info.price)
      
   statuses.append("Price: ${:,.2f} ( {:.2f} % )".format(info.price, price_percent_change))
   statuses.append("Market Cap: ${:,.0f}".format(info.total_coins * info.price))

   if previous_info != None and previous_info.price_alert_enabled and abs(price_percent_change) > PRICE_PERCENT_CHANGE_THRESHOLD:
      alerts.append("WARNING: Price change of {:.2f} %".format(price_percent_change))
      previous_info.price_alert_enabled = False
      
      
def write_history_stats(statuses, alerts, previous_info, info):
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()
   
   statuses.append("Historical Prices:")
   
   for years_ago in range(1, 6):
      history_info = price_history.get_historical_price(cursor, years_ago)
      old_date_str = history_info[0]
      old_price = history_info[1]

      old_price_str = "${:,.2f}".format(old_price)
      price_percent_change = price_history.percent_change(old_price, info.price)
      
      statuses.append("{} : {:>10} {:>10.2f} %".format(old_date_str, old_price_str, price_percent_change))

   connection.close()


def get_status(previous_info, info):
   statuses = []
   alerts = []

   write_block_stats(statuses, alerts, previous_info, info)
   statuses.append("")
   write_difficulty_stats(statuses, alerts, previous_info, info)
   write_reorg_stats(statuses, alerts, previous_info, info)
   statuses.append("")
   write_halving_stats(statuses, alerts, previous_info, info)
   statuses.append("")
   write_price_stats(statuses, alerts, previous_info, info)
   statuses.append("")
   write_history_stats(statuses, alerts, previous_info, info)
   
   status_string = "\n".join(statuses)
   has_alerts = len(alerts) > 0
   alert_string = "\n".join(alerts) + "\n\n" + status_string
   
   return (status_string, has_alerts, alert_string)
   
