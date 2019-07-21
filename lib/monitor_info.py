import smtplib
import sqlite3
import subprocess
import pickle
import time
import json
import requests
import os
from datetime import datetime, timedelta
from lib import reorg, price_history


HALVING_RATE = 210000 # mining reward halves after this many blocks
INITIAL_REWARD = 50.0

BLOCKS_PER_DAY = 144.0 # 6 per hour * 24 hours per day
BLOCKS_PER_WEEK = 1008.0 # 144 * 7
BLOCKS_PER_MONTH = 4032.0 # 1008 * 4


class Info:
   blocks = None
   headers = None
   price_alert_enabled = True


def get_info(previous_info):
   info = Info()
   info.last_status_time = datetime.now()
   
   block_info = json.loads(subprocess.check_output(['bitcoin-cli','getblockchaininfo']))
   info.blocks = block_info["blocks"]
   info.headers = block_info["headers"]
   
   mining_info = json.loads(subprocess.check_output(['bitcoin-cli','getmininginfo']))
   info.difficulty = mining_info["difficulty"]
   info.network_hash_rate = mining_info["networkhashps"]
   
   info.month_ago_block_time = get_block_time(round(info.blocks - BLOCKS_PER_MONTH))      
   info.week_ago_block_time = get_block_time(round(info.blocks - BLOCKS_PER_WEEK))
   info.day_ago_block_time = get_block_time(round(info.blocks - BLOCKS_PER_DAY))
   info.last_block_time = get_block_time(info.blocks)
   info.block_time_delta = datetime.now() - info.last_block_time

   priceResponse = requests.get("https://api.cryptowat.ch/markets/gdax/btcusd/price")
   info.price = priceResponse.json()['result']['price']
   
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
   
   cursor.execute("SELECT * FROM status_info ORDER BY date ASC limit 1")
   result = cursor.fetchone()


def write_info(info):
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()
   
   sql_command = "INSERT INTO status_info (date)\nVALUES (\"{}\", {}, {}, {}, {}, {}, {}, {});".format()
   cursor.execute(sql_command)

   connection.commit()
   connection.close()
