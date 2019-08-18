#!/usr/bin/python3

import sqlite3
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

USE_LOG_SCALE = True

# Open database connection
connection = sqlite3.connect("bitcoin.db")
cursor = connection.cursor()

# Candlestick fields
dates = []
open_data = []
high_data = []
low_data = []
close_data = []

# Process rows
cursor.execute("SELECT date, open, high, low, close FROM historical_prices ORDER BY date ASC")
result = cursor.fetchone()

while result != None:
    date = datetime.strptime(result[0], "%Y-%m-%d")
    dates.append(date)
    
    open_data.append(float(result[1]))
    high_data.append(float(result[2]))
    low_data.append(float(result[3]))
    close_data.append(float(result[4]))
    
    result = cursor.fetchone()

connection.close()

# Build chart
fig = go.Figure(data=[go.Candlestick(x=dates,
                       open=open_data, high=high_data,
                       low=low_data, close=close_data)])
                      
if USE_LOG_SCALE:
   fig.update_yaxes(type="log")

fig.show(renderer="browser")
