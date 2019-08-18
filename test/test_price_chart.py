import unittest
from charts import price_chart

class TestPriceChart(unittest.TestCase):
   
   def test_combine_rows_singleton(self):
      row = {"date": "2019-01-01", "open": 100, "high": 300, "low": 0, "close": 200}
      group = [row]
      self.assertEqual(row, price_chart.combine_rows(group))
      
   def test_combine_rows_multiple(self):
      row1 = {"date": "2019-01-01", "open": 1, "high": 2, "low": 1, "close": 2}
      row2 = {"date": "2019-01-02", "open": 2, "high": 5, "low": 1, "close": 4}
      row3 = {"date": "2019-01-03", "open": 4, "high": 4, "low": 1, "close": 4}
      row4 = {"date": "2019-01-04", "open": 4, "high": 4, "low": 0, "close": 3}
      group = [row1, row2, row3, row4]
      
      combined_row = {"date": "2019-01-01", "open": 1, "high": 5, "low": 0, "close": 3}
      self.assertEqual(combined_row, price_chart.combine_rows(group))
