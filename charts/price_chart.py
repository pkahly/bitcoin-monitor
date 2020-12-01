#!/usr/bin/python3

import plotly.graph_objects as go
from datetime import datetime
from lib import price_history


USE_LOG_SCALE = True
GROUPING = 60
START = datetime.timestamp(datetime.strptime("2015-08-10", "%Y-%m-%d"))
END = datetime.timestamp(datetime.strptime("2019-08-10", "%Y-%m-%d"))


def combine_rows(group):
   # Use starting date
   date = group[0]["date"]
   
   # Use first open
   open = group[0]["open"]
   
   # Use maximum high and minimum low
   high = group[0]["high"]
   low = group[0]["low"]
   for row in group:
      high = max(high, row["high"])
      low = min(low, row["low"])
   
   # Use last close
   close = group[-1]["close"]
   
   return {"date": date, "open": open, "high": high, "low": low, "close": close}


if __name__ == "__main__":
   # Candlestick fields
   dates = []
   open_data = []
   high_data = []
   low_data = []
   close_data = []

   # Extract data with grouping
   price_iter = price_history.PriceIterator(START, END)
   group = []

   for price_row in price_iter:
      # Add to group
      if len(group) < GROUPING:
         group.append(price_row)

      # Combine group into one candlestick
      else: 
         group_row = combine_rows(group)
         group = []
         
         dates.append(group_row["date"])
         open_data.append(group_row["open"])
         high_data.append(group_row["high"])
         low_data.append(group_row["low"])
         close_data.append(group_row["close"])

   # Build chart
   fig = go.Figure(data=[go.Candlestick(x=dates,
                          open=open_data, high=high_data,
                          low=low_data, close=close_data)], )
                         
   if USE_LOG_SCALE:
      fig.update_yaxes(type="log")
      

   fig.update_layout(xaxis_rangeslider_visible=False)
   fig.show(renderer="browser")
