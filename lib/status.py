import sqlite3
import subprocess
import requests
import os
from datetime import datetime, timedelta
from lib import reorg, price_history, monitor_info


BLOCK_REORG_THRESHOLD = 0
MINUTES_BETWEEN_BLOCKS_THRESHOLD = 90
PRICE_PERCENT_CHANGE_THRESHOLD = 10

BLOCKS_PER_DAY = 144.0 # 6 per hour * 24 hours per day
BLOCKS_PER_WEEK = 1008.0 # 144 * 7
BLOCKS_PER_MONTH = 4032.0 # 1008 * 4


def write_block_stats(statuses, alerts, previous_info, info):
   new_blocks = 0
   if previous_info != None:
      new_blocks = info.blocks - previous_info.blocks

   statuses.append("Blocks: {:,} ( + {} )".format(info.blocks, new_blocks))
   statuses.append("Last Block Time: {}".format(info.last_block_time.strftime("%m-%d %I:%M %p")))

   if info.blocks < info.headers:
      statuses.append("Headers: {} - Blocks Behind: {}".format(info.headers, (info.headers - info.blocks)))

   num_minutes = round(info.block_time_delta.total_seconds() / 60)
   if info.block_time_delta > timedelta(minutes=MINUTES_BETWEEN_BLOCKS_THRESHOLD):
      alerts.append("WARNING: No blocks in {} minutes".format(num_minutes))
   else:
      statuses.append("Minutes Since Last Block: {}".format(num_minutes))
      
      
def write_difficulty_stats(statuses, alerts, previous_info, info):
   difficulty_percent_change = 0
   hash_rate_percent_change = 0
   if previous_info != None:
      difficulty_percent_change = price_history.percent_change(previous_info.difficulty, info.difficulty)
      hash_rate_percent_change = price_history.percent_change(previous_info.network_hash_rate, info.network_hash_rate)
       
   statuses.append("Difficulty: {}".format(info.difficulty))
   statuses.append("Network Hash Rate: {} ( {:.2f} % )".format(info.network_hash_rate, hash_rate_percent_change))
   
   if difficulty_percent_change > 0:
      alerts.append("Difficulty Adjustment Occurred! Old: {} New: {} Change: {:.2f} %".format(previous_info.difficulty, info.difficulty, difficulty_percent_change))
      
   daily_avg = (info.last_block_time - info.day_ago_block_time).total_seconds() / BLOCKS_PER_DAY / 60
   weekly_avg = (info.last_block_time - info.week_ago_block_time).total_seconds() / BLOCKS_PER_WEEK / 60
   monthly_avg = (info.last_block_time - info.month_ago_block_time).total_seconds() / BLOCKS_PER_MONTH / 60
   statuses.append("Average time between blocks in last day: {:.2f} min".format(daily_avg))
   statuses.append("Average time between blocks in last week: {:.2f} min".format(weekly_avg))
   statuses.append("Average time between blocks in last month: {:.2f} min".format(monthly_avg))

   
def write_reorg_stats(statuses, alerts, previous_info, info):
   reorg_info = reorg.add_blocks()
   highest_stored_block = reorg_info["highest_stored_block"]
   last_matching_height = reorg_info["last_matching_height"]
   
   reorg_length = highest_stored_block - last_matching_height

   if reorg_length > BLOCK_REORG_THRESHOLD:
      alerts.append("WARNING: Block Reorg of {} blocks has occurred".format(reorg_length))


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
   
