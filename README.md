#### Note: Still under construction -- needs productionized, automated tests, etc. See open issues.

*Developed primarily for my own use, but feedback and contributions are welcome*

## Monitors a full Bitcoin node and sends status emails and alerts.

### Sample alerts:
```
TODO
```

### Sample status update:
```
Blocks: 590,508 ( + 21 )
Minutes Since Last Block: 1

Network Hash Rate: 67.80 EH/s ( 3.56 % )
Blocks until next difficulty adjustment: 180

Average time between blocks
Last day: 10.61 min
Last month: 9.38 min

Total Coins Mined: 17,881,362 ( 85.15 % )
Remaining Coins: 3,118,638

Current Reward: 12.5
Blocks Until Next Halving: 39,491 ( ~274 days )

Price: $10,405.79 ( 0.20 % )
Market Cap: $186.07 billion
```

### Sample daily summary:
```
Difference Since: 08-16 10:24 AM

Blocks: 590,517 ( + 124 )
Minutes Since Last Block: 5

Network Hash Rate: 68.95 EH/s ( -5.67 % )
Blocks until next difficulty adjustment: 171

Average time between blocks
Last day: 10.46 min
Last month: 9.39 min

Total Coins Mined: 17,881,475 ( 85.15 % )
Remaining Coins: 3,118,525

Current Reward: 12.5
Blocks Until Next Halving: 39,482 ( ~274 days )

Price: $10,327.64 ( 1.94 % )
Market Cap: $184.67 billion

All Time High Hash Rate: 88.4 EH/s
Lowest Recent Hash Rate: 44.7 EH/s

Historical Prices:
2018-08-17 :  $6,580.63      56.94 %
2017-08-17 :  $4,331.69     138.42 %
2016-08-17 :    $573.22    1701.69 %
2015-08-17 :    $257.98    3903.27 %
2014-08-17 :    $491.80    1999.97 %
```

### Set Up Instructions:

#### Run a full Bitcoin node. 
- https://bitcoincore.org/
- See the provided bitcoin.conf file for a sample configuration

#### Install sqlite3 and python-bitcoinrpc

#### Install the alerter. This will create a database of block info.
```
./main.py --install
```

#### *Optional* Import Historical Price Data.
```
./main.py --import_price_history
```

This will look for daily_history.csv in the current directory. The required format is as follows:
```
<date>,<open>,<high>,<low>,<close>
```

Example row:
```
Jul192019,10653.96,10716.98,10229.63,10530.73,20727426310,187725578628
```

I retrieved Mt. Gox data from https://bitcoincharts.com/charts/mtgoxUSD and recent aggregate data from https://coinmarketcap.com/

#### Edit the default config.json that was created automatically during the install. Format:
```
{
"enable_emails": false, 
"server": "", 
"port": "", 
"bot_email": "", 
"bot_password": "", 
"human_email": "", 
"bitcoind_user": "alerterbot", 
"bitcoind_pass": "DO_NOT_USE_76cf8e3a30fb29b4131a8babb", 
"use_testnet": false, 
"use_regtest": false, 
"status_frequency_in_hours": 6, 
"historical_price_filename": "daily_history.csv", 
"catch_errors": true, 
"block_reorg_threshold": 0, 
"minutes_between_blocks_threshold": 90, 
"price_percent_change_threshold": 5, 
"reorg_depth_cap": 5
}
```
- To receive emails, you must set *enable_emails* to true and provide values for *server*, *port*, *bot_email*, *bot_password* and *human_email*. Otherwise, output will only be logged to standard out.
- The use_testnet or use_regtest options can be used for testing this with a testnet or regtest Bitcoin node.

#### Start the Bitcoin Alerter
```
./main.py --run
```
