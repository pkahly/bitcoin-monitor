import time
from datetime import datetime, timedelta
from lib import info_collector, email, status, alerts, config_reader, time_tools

config = config_reader.get_config()
SECONDS_TO_SLEEP = config.minutes_to_sleep * 60

# Settings for exponential backoff, max is equal to the status frequency, or at least one hour
INITIAL_ERROR_SLEEP = SECONDS_TO_SLEEP
MAX_ERROR_SLEEP = max(3600 * config.status_frequency_in_hours, 3600)


def run_bitcoin_alerter():
   if config.catch_errors:
      _run_with_exponential_backoff()
   else:
      _run()


def _run():
   previous_info = info_collector.get_most_recent_info()
   
   while True:
      info = info_collector.get_info(previous_info)

      alert_list = alerts.get_alerts(previous_info, info)
   
      if len(alert_list) > 0:
         # Send alerts, with status
         status_string = status.get_status(previous_info, info)
         
         alert_string = "\n".join(alert_list) + "\n\n" + status_string
         
         email.send_email("Bitcoin ALERT", alert_string);
      elif previous_info == None or (datetime.now() - previous_info.last_status_time) > timedelta(hours=config.status_frequency_in_hours):
         # Send status
         status_string = status.get_status(previous_info, info)
         
         email.send_email("Bitcoin Status Update", status_string)
         
         previous_info = info
         info_collector.write_info(info)
      else:
         td = timedelta(hours=config.status_frequency_in_hours) - (datetime.now() - previous_info.last_status_time)
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
