import time
from datetime import datetime, timedelta
from lib import info_collector, email, status, alerts, config_reader

config = config_reader.get_config()
SECONDS_TO_SLEEP = config.minutes_to_sleep * 60
INITIAL_ERROR_SLEEP = SECONDS_TO_SLEEP

def run_bitcoin_alerter():
   previous_info = info_collector.get_most_recent_info()
   
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
         td = timedelta(hours=config.status_frequency_in_hours) - (datetime.now() - previous_info.last_status_time)
         hours, remainder = divmod(td.seconds, 3600)
         minutes, seconds = divmod(remainder, 60)
         print("No alerts. Next status email in: {}:{}:{}".format(hours, minutes, seconds))

      # Sleep
      time.sleep(SECONDS_TO_SLEEP)


def run_bitcoin_alerter_with_exponential_backoff():
   run_bitcoin_alerter() # TODO revert
   """  
   error_sleep = INITIAL_ERROR_SLEEP
   while True:
      try:
         run_bitcoin_alerter(previous_info)
         error_sleep = INITIAL_ERROR_SLEEP
      except Exception as ex:
         print(ex)
         try:
            email.send_email("Bitcoin Monitor Has Crashed", str(ex))
         except:
            print("Failed to send crash report")

      time.sleep(error_sleep)
      error_sleep *= 2
   """

