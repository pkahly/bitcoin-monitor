import unittest
from datetime import datetime
from lib import time_tools

class Object(object):
    pass


class TestTimeTools(unittest.TestCase):
   def test_seconds_to_hms(self):
      seconds = 3600 + 60 + 1
      correct_hms = (1, 1, 1)
      
      self.assertEqual(correct_hms, time_tools.seconds_to_hms(seconds))
      
      
   def test_get_timestamp_hours_ago(self):
      start_t = 1546304400
      past_t = 1546300800
      
      now = datetime.fromtimestamp(start_t)
      self.assertEqual(past_t, time_tools.get_timestamp_hours_ago(1, now))
   
   
   def test_should_send_daily_summary_True(self):
      config = Object()
      config.daily_summary_hour = 4
      
      last_status_time = Object()
      last_status_time.hour = 3
      
      now = Object()
      now.hour = 4
      
      self.assertTrue(time_tools.should_send_daily_summary(config, last_status_time, now))
      
      
   def test_should_send_daily_summary_False(self):
      config = Object()
      config.daily_summary_hour = 3
      
      last_status_time = Object()
      last_status_time.hour = 3
      
      now = Object()
      now.hour = 4
      
      self.assertFalse(time_tools.should_send_daily_summary(config, last_status_time, now))
