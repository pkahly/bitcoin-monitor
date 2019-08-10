import unittest
from lib import alerts, info_collector

class TestAlerts(unittest.TestCase):
   def setUp(self):
      self.info = self._get_default_info()
      self.previous_info = self._get_default_info()
      
   def test_blocks(self):
      self.info.num_minutes = 9999
      alert_list = alerts.get_alerts(self.previous_info, self.info)
      self.assertTrue('WARNING: No blocks in 9999 minutes' in alert_list)
      
   def test_difficulty(self):
      self.info.difficulty_percent_change = 10
      alert_list = alerts.get_alerts(self.previous_info, self.info)
      self.assertTrue('Difficulty Adjustment Occurred! Old: 100 New: 100 Change: 10.00 %' in alert_list)
      
   def test_reorg(self):
      self.info.reorg_length = 100
      alert_list = alerts.get_alerts(self.previous_info, self.info)
      self.assertTrue('WARNING: Block Reorg of 100 blocks has occurred' in alert_list)

   def test_price(self):
      self.info.price_percent_change = 1000
      alert_list = alerts.get_alerts(self.previous_info, self.info)
      self.assertTrue('WARNING: Price change of 1000.00 %' in alert_list)
      
   def _get_default_info(self):
      info = info_collector.Info()
      info.num_minutes = 0
      info.difficulty = 100
      info.difficulty_percent_change = 0
      info.reorg_length = 0
      info.price_percent_change = 0
      return info
