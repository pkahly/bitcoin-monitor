from datetime import datetime

commas_to_word = {
   0: "",
   1: "thousand",
   2: "million",
   3: "billion",
   4: "trillion",
   5: "quadrillion"
}

def percent_change(start, end):
   start = float(start)
   end = float(end)
   return (end - start) / start * 100
   
def to_human_readable_large_number(number):
   num_commas = 0
   while number >= 1000:
      number /= 1000
      num_commas += 1
      
   number = round(number, 2)
   word = commas_to_word[num_commas]
   return "{} {}".format(number, word)

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
      print("No price data for {}".format(old_date_str))
      return None
