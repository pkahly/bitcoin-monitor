#!/usr/bin/python3

import sqlite3
from statistics import mean
import plotly.graph_objects as go

DAY = 144
WEEK = 1008
MONTH = 4032
YEAR = 52560

USE_LOG_SCALE = True
GROUPING = YEAR

def combine_group(group):
   # Use first height
   height = group[0][0]
   
   # Use mean of hashrates   
   hashrates = [result[1] for result in group]
   hashrate = int(mean(hashrates));
   
   return (height, hashrate)

if __name__ == "__main__":
   # Chart fields
   blocks = []
   hashrates = []

   # Collect Historical Hashrates
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()
   
   # Exclude genesis block as its networkhashps is very high
   cursor.execute("SELECT height, networkhashps FROM block_info WHERE height > 0 ORDER BY height ASC")
   
   result = cursor.fetchone()
   group = []
   
   while result != None:
      # Add to group
      if len(group) < GROUPING:
         group.append(result)
         
      # Else combine group into a mean
      else:
         height, hashrate = combine_group(group)
         group = []
         
         blocks.append(height)
         hashrates.append(hashrate)
         
      result = cursor.fetchone()

   connection.close()

   # Build chart
   fig = go.Figure(data=[go.Scatter(x=blocks, y=hashrates)], )
   
   if USE_LOG_SCALE:
      fig.update_yaxes(type="log")
                         
   fig.update_layout(xaxis_rangeslider_visible=False)
   fig.show(renderer="browser")
