from datetime import datetime

def percent_change(start, end):
   return (end - start) / start * 100

def get_historical_price(cursor, years_ago):
   old_date = datetime.now()
   
   try:
      old_date = old_date.replace(year=old_date.year - years_ago)
   except ValueError:
      # Correct for February 29 on leap years
      old_date = old_date.replace(day=old_date.day - 1, year=old_date.year - years_ago)
   
   old_date_str = old_date.strftime("%Y-%m-%d")

   cursor.execute("SELECT close FROM historical_prices WHERE date = \"{}\"".format(old_date_str))
   old_price = cursor.fetchone()[0]
   
   return (old_date_str, old_price)
