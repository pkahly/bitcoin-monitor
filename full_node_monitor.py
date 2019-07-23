#!/usr/bin/python3


import sqlite3
import subprocess
import time
import json
import requests
import os
from datetime import datetime, timedelta
from lib import reorg, price_history, info_collector, email, status, alerts


# Configuration
MINUTES_TO_SLEEP = 5
SECONDS_TO_SLEEP = MINUTES_TO_SLEEP * 60
INITIAL_ERROR_SLEEP = SECONDS_TO_SLEEP
STATUS_FREQUENCY_IN_HOURS = 4


def run_bitcoin_alerter():
   previous_info = info_collector.get_most_recent_info()
   last_run = previous_info.last_status_time.strftime("%m-%d %I:%M %p")
      
   #email.send_email("Bitcoin Monitor Online", "Bitcoin Monitor has just started. Last status email was at {}\n".format(last_run))

   while True:
      info = info_collector.get_info(previous_info)
      
      status_string = status.get_status(previous_info, info)
      alert_list = alerts.get_alerts(previous_info, info)
   
      alert_string = "\n".join(alert_list) + "\n\n" + status_string
   
      # Send Status Email
      if len(alert_list) > 0:
         email.send_email("Bitcoin ALERT", alert_string);
      elif previous_info == None or (datetime.now() - previous_info.last_status_time) > timedelta(hours=STATUS_FREQUENCY_IN_HOURS):
         email.send_email("Bitcoin Status Update", status_string)
         previous_info = info
         info_collector.write_info(info)
      else:
         td = timedelta(hours=STATUS_FREQUENCY_IN_HOURS) - (datetime.now() - previous_info.last_status_time)
         hours, remainder = divmod(td.seconds, 3600)
         minutes, seconds = divmod(remainder, 60)
         print("No alerts. Next status email in: {}:{}:{}".format(hours, minutes, seconds))

      # Sleep
      time.sleep(SECONDS_TO_SLEEP)



############################################################################


error_sleep = INITIAL_ERROR_SLEEP
while True:
   try:
      run_bitcoin_alerter()
      error_sleep = INITIAL_ERROR_SLEEP
   except Exception as ex:
      email.send_email("Bitcoin Monitor Has Crashed", str(ex))

   time.sleep(error_sleep)
   error_sleep *= 2
