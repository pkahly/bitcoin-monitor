

def seconds_to_hms(total_seconds):
   hours, remainder = divmod(total_seconds, 3600)
   minutes, seconds = divmod(remainder, 60)
   
   return (hours, minutes, seconds)
