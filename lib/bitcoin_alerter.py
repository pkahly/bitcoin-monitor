import time
from datetime import datetime, timedelta
from lib import info_collector, email, status, alerts, config_reader, time_tools

config = config_reader.get_config()
SECONDS_TO_SLEEP = 600 # 10 minutes

# Settings for exponential backoff
INITIAL_ERROR_SLEEP = 600 # 10 minutes
MAX_ERROR_SLEEP = 14400 # 4 hours


def run_bitcoin_alerter():
   if config.catch_errors:
      _run_with_exponential_backoff()
   else:
      _run()


def _run():
   while True:
      previous_info = info_collector.get_most_recent_info()
      info = info_collector.get_info(previous_info)
      
      alert_list = alerts.get_alerts(previous_info, info)
      
      if previous_info == None:
         # Write info and sleep
         info_collector.write_info(info)
         
      elif len(alert_list) > 0:
         # Send alerts and status
         send_alert(previous_info, info, alert_list)
      
      elif time_tools.should_send_daily_summary(config, previous_info.status_time, datetime.now()):
         # TODO determine if we should send a daily summary
         send_daily_summary()
      
      elif (datetime.now() - previous_info.status_time) > timedelta(hours=config.status_frequency_in_hours):
         # Send status
         send_status(previous_info, info)
      
      else:
         td = timedelta(hours=config.status_frequency_in_hours) - (datetime.now() - previous_info.status_time)
         hours, minutes, seconds = time_tools.seconds_to_hms(td.seconds)
         print("No alerts. Next status email in: {}:{}:{}".format(hours, minutes, seconds))
         
      # Sleep
      time.sleep(SECONDS_TO_SLEEP)


def _run_with_exponential_backoff():
   error_sleep = INITIAL_ERROR_SLEEP
   while True:
      try:
         _run()
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
      
      
def send_alert(previous_info, info, alert_list):
   status_string = status.get_status(previous_info, info)
   alert_string = "\n".join(alert_list) + "\n\n" + status_string

   email.send_email("Bitcoin ALERT", alert_string);

   info_collector.write_info(info)
   

def send_status(previous_info, info):
   status_string = status.get_status(previous_info, info)

   email.send_email("Bitcoin Status Update", status_string)

   info_collector.write_info(info)
   
   
def send_daily_summary():
   previous_info = info_collector.get_closest_info_to_timestamp(time_tools.get_timestamp_hours_ago(24, datetime.now()))
   if previous_info == None:
      return
   
   info = info_collector.get_info(previous_info)
   summary = status.get_daily_summary(previous_info, info)
   
   email.send_email("Bitcoin Daily Summary", summary)
   
   info_collector.write_info(info)
