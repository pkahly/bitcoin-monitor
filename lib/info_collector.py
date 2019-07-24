import sqlite3
import subprocess
import json
import requests
from datetime import datetime
from lib import reorg, price_history


HALVING_RATE = 210000 # mining reward halves after this many blocks
INITIAL_REWARD = 50.0

BLOCKS_PER_DAY = 144.0 # 6 per hour * 24 hours per day
BLOCKS_PER_WEEK = 1008.0 # 144 * 7
BLOCKS_PER_MONTH = 4032.0 # 1008 * 4


class Info:
   last_status_time = datetime.now()
   blocks = None
   headers = None
   difficulty = None
   network_hash_rate = None
   month_ago_block_time = None
   week_ago_block_time = None
   day_ago_block_time = None
   last_block_time = None
   block_time_delta = None
   price = None
   reward = None
   total_coins = None
   blocks_till_halving = None
   days_till_halving = None
   price_alert_enabled = True


def get_info(previous_info):
   info = Info()
   info.last_status_time = datetime.now()
   
   info.blocks = json.loads(subprocess.check_output(['bitcoin-cli','getblockcount']))
   info.new_blocks = 0
   
   if previous_info != None:
      info.new_blocks = info.blocks - previous_info.blocks
   
   mining_info = json.loads(subprocess.check_output(['bitcoin-cli','getmininginfo']))
   info.difficulty = mining_info["difficulty"]
   info.network_hash_rate = mining_info["networkhashps"]
   
   info.difficulty_percent_change = 0
   info.hash_rate_percent_change = 0
   if previous_info != None:
      info.difficulty_percent_change = price_history.percent_change(previous_info.difficulty, info.difficulty)
      info.hash_rate_percent_change = price_history.percent_change(previous_info.network_hash_rate, info.network_hash_rate)
   
   month_ago_block_time = get_block_time(round(info.blocks - BLOCKS_PER_MONTH))      
   week_ago_block_time = get_block_time(round(info.blocks - BLOCKS_PER_WEEK))
   day_ago_block_time = get_block_time(round(info.blocks - BLOCKS_PER_DAY))
   info.last_block_time = get_block_time(info.blocks)
      
   info.daily_avg = (info.last_block_time - day_ago_block_time).total_seconds() / BLOCKS_PER_DAY / 60
   info.weekly_avg = (info.last_block_time - week_ago_block_time).total_seconds() / BLOCKS_PER_WEEK / 60
   info.monthly_avg = (info.last_block_time - month_ago_block_time).total_seconds() / BLOCKS_PER_MONTH / 60
   
   block_time_delta = datetime.now() - info.last_block_time
   info.num_minutes = round(block_time_delta.total_seconds() / 60)
   
   reorg_info = reorg.add_blocks()
   highest_stored_block = reorg_info["highest_stored_block"]
   last_matching_height = reorg_info["last_matching_height"]
   
   info.reorg_length = highest_stored_block - last_matching_height

   priceResponse = requests.get("https://api.cryptowat.ch/markets/gdax/btcusd/price")
   info.price = priceResponse.json()['result']['price']
   
   info.price_percent_change = 0
   if previous_info != None:
       info.price_percent_change = price_history.percent_change(previous_info.price, info.price)
   
   info.reward = INITIAL_REWARD
   info.total_coins = 0
   remaining_blocks = info.blocks + 1 # Add one because blocks is 0-based
   
   while remaining_blocks >= HALVING_RATE:
      info.total_coins += info.reward * HALVING_RATE
      info.reward /= 2
      remaining_blocks -= HALVING_RATE
   
   info.total_coins += info.reward * remaining_blocks
   info.blocks_till_halving = HALVING_RATE - remaining_blocks
   info.days_till_halving = info.blocks_till_halving / BLOCKS_PER_DAY
      
   return info
   
   
def get_block_time(block_height):
   block_stats = json.loads(subprocess.check_output(['bitcoin-cli','getblockstats',str(block_height),json.dumps(["time"])]))
   return datetime.fromtimestamp(block_stats["time"])


def get_most_recent_info():
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()
   
   cursor.execute("SELECT timestamp, blocks, difficulty, network_hash_rate, price FROM status_info ORDER BY timestamp DESC limit 1")
   result = cursor.fetchone()
   
   if result == None:
      return None
   
   info = Info()
   info.last_status_time = datetime.fromtimestamp(result[0])
   info.blocks = result[1]
   info.difficulty = result[2]
   info.network_hash_rate = result[3]
   info.price = result[4]
   return info


def write_info(info):
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()
   
   timestamp = round(datetime.timestamp(info.last_status_time))

   sql_command = "INSERT INTO status_info (timestamp, blocks, difficulty, network_hash_rate, price)\nVALUES ({}, {}, {}, {}, {});".format(timestamp, info.blocks, info.difficulty, info.network_hash_rate, info.price)
   cursor.execute(sql_command)

   connection.commit()
   connection.close()
