import sqlite3
from datetime import datetime
import logging

NUMBER_WORD_DICT = {
   0: "",
   1: "thousand",
   2: "million",
   3: "billion",
   4: "trillion",
   5: "quadrillion"
}

HASHES_WORD_DICT = {
   0: "H/s",
   1: "KH/s",
   2: "MH/s",
   3: "GH/s",
   4: "TH/s",
   5: "PH/s",
   6: "EH/s",
   7: "ZH/s"
}

def percent_change(start, end):
   start = float(start)
   end = float(end)
   return (end - start) / start * 100
   
def to_human_readable_large_number(number, word_dict):
   num_commas = 0
   while number >= 1000:
      number /= 1000
      num_commas += 1
      
   number = round(number, 2)
   word = word_dict[num_commas]
   return "{} {}".format(number, word)
   
def get_all_historical_prices(current_price):
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()
   
   prices = []
   for years_ago in range(1, 50):
      history_info = get_historical_price(cursor, years_ago)
      if history_info == None:
         break
      
      old_date_str = history_info[0]
      old_price = history_info[1]

      old_price_str = "${:,.2f}".format(old_price)
      price_percent_change = percent_change(old_price, current_price)
      
      prices.append("{} : {:>15} {:>15.2f} %".format(old_date_str, old_price_str, price_percent_change))

   connection.close()
   return prices

def get_historical_price(cursor, years_ago):
   old_date = datetime.now()
   
   try:
      old_date = old_date.replace(year=old_date.year - years_ago)
   except ValueError:
      # Correct for February 29 on leap years
      old_date = old_date.replace(day=old_date.day - 1, year=old_date.year - years_ago)
   
   old_date_str = old_date.strftime("%Y-%m-%d")

   cursor.execute("SELECT close FROM historical_prices WHERE date = \"{}\"".format(old_date_str))
   result = cursor.fetchone()
   
   if result != None:
      old_price = result[0]
      return (old_date_str, old_price)
   else:
      logging.info("No price data for {}".format(old_date_str))
      return None
      

# Iterator for the price_history table
# Returns a dict containing date and OHLC data

class PriceIterator:
   def __init__(self, start, end):
      connection = sqlite3.connect("bitcoin.db")
      self.cursor = connection.cursor()
      self.cursor.execute("SELECT date, open, high, low, close FROM historical_prices WHERE timestamp > {} AND timestamp < {} ORDER BY date ASC".format(int(start), int(end)))

   def __next__(self):
      result = self.cursor.fetchone()
      if not result:
         raise StopIteration
      
      date = datetime.strptime(result[0], "%Y-%m-%d")

      open = float(result[1])
      high = float(result[2])
      low = float(result[3])
      close = float(result[4])
      
      return {"date": date, "open": open, "high": high, "low": low, "close": close}

   def __iter__(self):
      return self
