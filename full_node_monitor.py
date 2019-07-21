#!/usr/bin/python3


import smtplib
import sqlite3
import subprocess
import pickle
import time
import json
import requests
import os
from datetime import datetime, timedelta
from lib import reorg, price_history, monitor_info


# Configuration
MINUTES_TO_SLEEP = 5
SECONDS_TO_SLEEP = MINUTES_TO_SLEEP * 60
INITIAL_ERROR_SLEEP = SECONDS_TO_SLEEP
STATUS_FREQUENCY_IN_HOURS = 4

BLOCK_REORG_THRESHOLD = 0
MINUTES_BETWEEN_BLOCKS_THRESHOLD = 90
PRICE_PERCENT_CHANGE_THRESHOLD = 10

with open('config.json') as json_file:
   config = json.load(json_file)
   SERVER = config["SERVER"]
   PORT = config["PORT"]
   BOT_EMAIL = config["BOT_EMAIL"]
   BOT_PASSWORD = config["BOT_PASSWORD"]
   HUMAN_EMAIL = config["HUMAN_EMAIL"]

BLOCKS_PER_DAY = 144.0 # 6 per hour * 24 hours per day
BLOCKS_PER_WEEK = 1008.0 # 144 * 7
BLOCKS_PER_MONTH = 4032.0 # 1008 * 4


def send_email(subject, message):
   # Start SMTP server
   server = smtplib.SMTP_SSL(SERVER,port=PORT)
   server.ehlo()
   server.login(BOT_EMAIL, BOT_PASSWORD)

   dt = datetime.today()

   # Send email
   email_text = "Subject: {} {}\n\n{}".format(subject, dt.strftime("%m-%d"), message)
   #server.sendmail(BOT_EMAIL, HUMAN_EMAIL, email_text)

   print("\n\n###################################\n")
   print(email_text)
   print()

   # Stop SMTP Server
   server.quit()


def write_block_stats(statuses, alerts, previous_info, info):
   new_blocks = 0
   if previous_info != None:
      new_blocks = info.blocks - previous_info.blocks

   statuses.append("Blocks: {:,} ( + {} )".format(info.blocks, new_blocks))
   statuses.append("Last Block Time: {}".format(info.last_block_time.strftime("%m-%d %H:%M")))

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


## Main Loop ##
def run_bitcoin_alerter():
   previous_info = monitor_info.get_most_recent_info()
   last_run = previous_info.last_status_time.strftime("%m-%d %H:%M")
      
   #send_email("Bitcoin Monitor Online", "Bitcoin Monitor has just started. Last status email was at {}\n".format(last_run))

   while True:
      statuses = []
      alerts = []

      info = monitor_info.get_info(previous_info)

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
      alert_string = "\n".join(alerts) + "\n\n" + status_string

      # Send Status Email
      if len(alerts) > 0:
         send_email("Bitcoin ALERT", alert_string);
      elif previous_info == None or (datetime.now() - previous_info.last_status_time) > timedelta(hours=STATUS_FREQUENCY_IN_HOURS):
         send_email("Bitcoin Status Update", status_string)
         previous_info = info
         pickle.dump(info, open(PICKLE_FILE, "wb"))
      else:
         td = timedelta(hours=STATUS_FREQUENCY_IN_HOURS) - (datetime.now() - previous_info.last_status_time)
         hours, remainder = divmod(td.seconds, 3600)
         minutes, seconds = divmod(remainder, 60)
         print("No alerts. Next status email in: {}:{}:{}".format(hours, minutes, seconds))

      # Sleep
      time.sleep(SECONDS_TO_SLEEP)



############################################################################

run_bitcoin_alerter()
"""
error_sleep = INITIAL_ERROR_SLEEP
while True:
   try:
      run_bitcoin_alerter()
      error_sleep = INITIAL_ERROR_SLEEP
   except Exception as ex:
      send_email("Bitcoin Monitor Has Crashed", str(ex))

   time.sleep(error_sleep)
   error_sleep *= 2
"""
