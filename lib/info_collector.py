import sqlite3
import json
import requests
from datetime import datetime
from lib import reorg, price_history, bitcoin_node_api


HALVING_RATE = 210000 # mining reward halves after this many blocks
INITIAL_REWARD = 50.0
MAX_COINS = 21000000

BLOCKS_PER_DAY = 144 # 6 per hour * 24 hours per day
BLOCKS_PER_WEEK = 1008 # 144 * 7
BLOCKS_PER_MONTH = 4032 # 1008 * 4
DIFFICULTY_PERIOD = 2016

class Info:
   def __init__(self):
      self.status_time = datetime.now()


def get_info(previous_info):
   info = Info()
   bitcoin_client = bitcoin_node_api.BitcoinAPIClient()
   
   info.blocks = bitcoin_client.get_num_blocks()
   headers = bitcoin_client.get_num_headers()
   if info.blocks != headers:
      raise RuntimeError("Verifying Blocks: {} / {}".format(info.blocks, headers))

   info.new_blocks = info.blocks
   if previous_info != None:
      info.new_blocks = info.blocks - previous_info.blocks
      
   last_block_time = datetime.fromtimestamp(bitcoin_client.get_blockstats(info.blocks, "time"))
   block_time_delta = datetime.now() - last_block_time
   info.num_minutes = round(block_time_delta.total_seconds() / 60)
   
   mining_info = bitcoin_client.get_mining_info()
   info.difficulty = mining_info["difficulty"]
   info.network_hash_rate = bitcoin_client.get_network_hashrate(BLOCKS_PER_DAY)
   
   blocks_since_difficulty_adjustment = info.blocks % DIFFICULTY_PERIOD
   info.blocks_till_difficulty_adjustment = DIFFICULTY_PERIOD - blocks_since_difficulty_adjustment
   
   info.difficulty_percent_change = 0
   info.hash_rate_percent_change = 0
   if previous_info != None:
      info.difficulty_percent_change = price_history.percent_change(previous_info.difficulty, info.difficulty)
      info.hash_rate_percent_change = price_history.percent_change(previous_info.network_hash_rate, info.network_hash_rate)
   
   info.daily_avg = get_average_block_time(bitcoin_client, info.blocks, BLOCKS_PER_DAY)
   info.weekly_avg = get_average_block_time(bitcoin_client, info.blocks, BLOCKS_PER_WEEK)
   info.monthly_avg = get_average_block_time(bitcoin_client, info.blocks, BLOCKS_PER_MONTH)
   
   reorg_info = reorg.add_blocks(bitcoin_client)
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

   info.remaining_coins = MAX_COINS - info.total_coins   
   info.coins_mined_percent = (info.total_coins / MAX_COINS) * 100
      
   return info
   
   
def get_average_block_time(bitcoin_client, end_block, depth):
   start_block = end_block - depth

   if start_block < 0:
      return 0

   end_time = datetime.fromtimestamp(bitcoin_client.get_blockstats(end_block, "mediantime"))
   start_time = datetime.fromtimestamp(bitcoin_client.get_blockstats(start_block, "mediantime"))
   
   return (end_time - start_time).total_seconds() / depth / 60
   
   
def get_most_recent_info():
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()
   
   cursor.execute("SELECT timestamp, blocks, difficulty, network_hash_rate, price FROM status_info ORDER BY timestamp DESC limit 1")
   result = cursor.fetchone()
   
   if result == None:
      return None
   
   info = Info()
   info.status_time = datetime.fromtimestamp(result[0])
   info.blocks = result[1]
   info.difficulty = result[2]
   info.network_hash_rate = result[3]
   info.price = result[4]
   return info


def write_info(info):
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()
   
   timestamp = int(datetime.timestamp(info.status_time)) # truncate the microsecond portion

   sql_command = "INSERT INTO status_info (timestamp, blocks, difficulty, network_hash_rate, price)\nVALUES ({}, {}, {}, {}, {});".format(timestamp, info.blocks, info.difficulty, info.network_hash_rate, info.price)
   cursor.execute(sql_command)

   connection.commit()
   connection.close()
