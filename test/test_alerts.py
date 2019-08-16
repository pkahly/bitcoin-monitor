import unittest
from lib import alerts, info_collector

class TestAlerts(unittest.TestCase):
   def setUp(self):
      self.info = self._get_default_info()
      self.previous_info = self._get_default_info()
      
   def test_blocks(self):
      self.info.num_minutes = 9999
      alert_list = alerts.get_alerts(self.previous_info, self.info)
      self.assertTrue('No blocks in 9999 minutes' in alert_list)
      
   def test_difficulty(self):
      self.info.difficulty_percent_change = 10
      alert_list = alerts.get_alerts(self.previous_info, self.info)
      self.assertTrue('Difficulty Adjustment Occurred! Old: 100 New: 100 Change: 10.00 %' in alert_list)
      
   def test_reorg(self):
      self.info.reorg_length = 100
      alert_list = alerts.get_alerts(self.previous_info, self.info)
      self.assertTrue('Block Reorg of 100 blocks has occurred' in alert_list)

   def test_price(self):
      self.info.price_percent_change = 1000
      alert_list = alerts.get_alerts(self.previous_info, self.info)
      self.assertTrue('Price change of 1000.00 %' in alert_list)
      
   def test_max_hashrate(self):
      self.info.network_hash_rate = 20
      self.info.max_hash_rate = 10
      alert_list = alerts.get_alerts(self.previous_info, self.info)
      self.assertTrue('Above Maximum Hash Rate: 20 H/s > 10 H/s' in alert_list)
      
   def test_min_hashrate(self):
      self.info.network_hash_rate = 5
      self.info.min_hash_rate = 10
      alert_list = alerts.get_alerts(self.previous_info, self.info)
      self.assertTrue('Below Local Minimum Hash Rate: 5 H/s < 10 H/s' in alert_list)
      
   def test_high_blocktime(self):
      self.info.daily_avg = 12.1
      alert_list = alerts.get_alerts(self.previous_info, self.info)
      self.assertTrue('Unusual Block Time: 12.1 min' in alert_list)
      
   def test_low_blocktime(self):
      self.info.daily_avg = 7.9
      alert_list = alerts.get_alerts(self.previous_info, self.info)
      self.assertTrue('Unusual Block Time: 7.9 min' in alert_list)
      
   def _get_default_info(self):
      info = info_collector.Info()
      info.num_minutes = 0
      info.difficulty = 100
      info.difficulty_percent_change = 0
      info.reorg_length = 0
      info.price_percent_change = 0
      info.network_hash_rate = 10
      info.max_hash_rate = 20
      info.min_hash_rate = 5
      info.daily_avg = 10
      return info
