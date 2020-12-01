import time, traceback
from datetime import datetime, timedelta
from lib import info_collector, email, status, alerts, time_tools, watchlist
import logging

SECONDS_TO_SLEEP = 600 # 10 minutes
INITIAL_ERROR_SLEEP = 600 # 10 minutes
MAX_ERROR_SLEEP = 14400 # 4 hours


def run_bitcoin_alerter(config):
   alertgen = alerts.AlertGenerator(config)
   
   if config.catch_errors:
      _run_with_exponential_backoff(config, alertgen)
   else:
      _run(config, alertgen)


def _run(config, alertgen):
   while True:
      previous_info = info_collector.get_most_recent_info()
      info = info_collector.get_info(config, previous_info)
      
      alert_list = alertgen.get_alerts(previous_info, info)
      
      if previous_info == None:
         # Write info and sleep
         info_collector.write_info(info)
         logging.info("Initialized status table. Sleep {} seconds".format(SECONDS_TO_SLEEP))
         
      elif len(alert_list) > 0:
         # Send alerts
         send_alert(config, alert_list)
      
      elif time_tools.should_send_daily_summary(config, previous_info.status_time, datetime.now()):
         send_daily_summary(config)
      
      elif (datetime.now() - previous_info.status_time) > timedelta(hours=config.status_frequency_in_hours):
         # Send status
         send_status(config, previous_info, info)
      
      else:
         td = timedelta(hours=config.status_frequency_in_hours) - (datetime.now() - previous_info.status_time)
         hours, minutes, seconds = time_tools.seconds_to_hms(td.seconds)
         logging.info("No alerts. Next status email in: {}:{}:{}".format(hours, minutes, seconds))
      
      # Sleep
      time.sleep(SECONDS_TO_SLEEP)


def _run_with_exponential_backoff(config, alertgen):
   error_sleep = INITIAL_ERROR_SLEEP
   while True:
      try:
         _run(config, alertgen)
         error_sleep = INITIAL_ERROR_SLEEP
      except info_collector.VerifyingBlocks as ex:
         # If we are still verifying blocks, print the progress
         # Do not send a crash report or print the stack trace
         logging.info(ex)
      except Exception as ex:
         # Print stack trace
         #traceback.print_exc()
         logging.error(ex)
         
         # Attempt to send a crash report
         try:
            email.send_email(config, "Bitcoin Monitor Has Crashed", traceback.format_exc())
         except Exception as ex:
            logging.error("Failed to send crash report")
            #traceback.print_exc()
            logging.error(ex)

      hours, minutes, seconds = time_tools.seconds_to_hms(error_sleep)
      logging.info("Retry in {}:{}".format(hours, minutes))
      
      time.sleep(error_sleep)
      error_sleep = min(error_sleep * 2, MAX_ERROR_SLEEP)
      
      
def send_alert(config, alert_list):
   alert_string = "\n".join(alert_list)
   email.send_email(config, "Bitcoin ALERT", alert_string);
   

def send_status(config, previous_info, info):
   status_string = status.get_status(previous_info, info)

   email.send_email(config, "Bitcoin Status Update", status_string)

   info_collector.write_info(info)
   
   
def send_daily_summary(config):
   previous_info = info_collector.get_closest_info_to_timestamp(time_tools.get_timestamp_hours_ago(24, datetime.now()))
   if previous_info == None:
      logging.info("No saved info, cannot send daily summary")
      return
   
   info = info_collector.get_info(config, previous_info)
   spent_utxo = watchlist.check_watchlist(config)
   
   summary = status.get_daily_summary(previous_info, info, spent_utxo)
   email.send_email(config, "Bitcoin Daily Summary", summary)
   
   info_collector.write_info(info)
   watchlist.remove_all_from_watchlist(spent_utxo)
