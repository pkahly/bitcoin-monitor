from datetime import datetime, timedelta

def seconds_to_hms(total_seconds):
   hours, remainder = divmod(total_seconds, 3600)
   minutes, seconds = divmod(remainder, 60)
   
   return (hours, minutes, seconds)
   
   
def get_timestamp_hours_ago(hours, now):
   timestamp = int(datetime.timestamp(now - timedelta(hours=hours))) # truncate the microsecond portion
   return timestamp
   
   
def should_send_daily_summary(config, last_status_time, now):
   # last_status_time < daily_summary_hour = now
   return last_status_time.hour < config.daily_summary_hour and config.daily_summary_hour == now.hour
