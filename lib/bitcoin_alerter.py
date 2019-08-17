import time
from datetime import datetime, timedelta
from lib import info_collector, email, status, alerts, time_tools

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
         print("Initialized status table. Sleep {} seconds".format(SECONDS_TO_SLEEP))
         
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
         print("No alerts. Next status email in: {}:{}:{}".format(hours, minutes, seconds))
      
      # Sleep
      time.sleep(SECONDS_TO_SLEEP)


def _run_with_exponential_backoff(config, alertgen):
   error_sleep = INITIAL_ERROR_SLEEP
   while True:
      try:
         _run(config, alertgen)
         error_sleep = INITIAL_ERROR_SLEEP
      except Exception as ex:
         print(ex)
         try:
            email.send_email("Bitcoin Monitor Has Crashed", str(ex))
         except:
            print("Failed to send crash report")

      hours, minutes, seconds = time_tools.seconds_to_hms(error_sleep)
      print("Retry in {}:{}".format(hours, minutes))
      
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
      return
   
   info = info_collector.get_info(config, previous_info)
   summary = status.get_daily_summary(previous_info, info)
   
   email.send_email(config, "Bitcoin Daily Summary", summary)
   
   info_collector.write_info(info)
