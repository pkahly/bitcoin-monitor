#!/usr/bin/python3

import sqlite3
import plotly.graph_objects as go


if __name__ == "__main__":
   # Chart fields
   blocks = []
   hashrates = []

   # Collect Historical Hashrates
   connection = sqlite3.connect("bitcoin.db")
   cursor = connection.cursor()
   cursor.execute("SELECT height, networkhashps FROM block_info ORDER BY height ASC")
   
   result = cursor.fetchone()
   while result != None:
      height = result[0]
      hashrate = result[1]
      
      blocks.append(height)
      hashrates.append(hashrate)
      
      result = cursor.fetchone()

   connection.close()

   # Build chart
   fig = go.Figure(data=[go.Scatter(x=blocks, y=hashrates)], )
                         
   fig.update_layout(xaxis_rangeslider_visible=False)
   fig.show(renderer="browser")
