#### Note: Still under construction -- needs productionized, automated tests, etc. See open issues.

## Monitors a full Bitcoin node and sends status emails and alerts.

### Sample status contents:
```
Blocks: 589,416 ( + 33 )
Last Block Time: 08-09 10:49 PM
Minutes Since Last Block: 5

Difficulty: 9,985,348,008,060
Network Hash Rate: 71.74 EH/s ( 1.09 % )
Blocks until next difficulty adjustment: 744

Average time between blocks
Last day: 9.86 min
Last week: 9.28 min
Last month: 9.45 min

Total Coins Mined: 17,867,712 ( 85.08 % )
Remaining Coins: 3,132,288
Current Reward: 12.5
Blocks Until Next Halving: 40,583 ( ~282 days )

Price: $11,801.51 ( -0.79 % )
Market Cap: $210.87 billion

Historical Prices:
2018-08-09 :  $6,568.23      79.68 %
2017-08-09 :  $3,342.47     253.08 %
2016-08-09 :    $587.80    1907.74 %
2015-08-09 :    $265.08    4352.06 %
2014-08-09 :    $589.37    1902.39 %
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
<Date>,<open>,<high>,<low>,<close>,<volume>,<market cap>
```

Example row:
```
Jul192019,10653.96,10716.98,10229.63,10530.73,20727426310,187725578628
```

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
"minutes_to_sleep": 5, 
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
