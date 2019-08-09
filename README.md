#### Note: Still under construction -- needs productionized, automated tests, etc. See open issues.

## Monitors a full Bitcoin node and sends status emails and alerts.

### Sample status contents:
	Blocks: 586,433 ( + 28 )
	Last Block Time: 07-21 17:53
	Minutes Since Last Block: 6

	Difficulty: 9064159826491.41
	Network Hash Rate: 6.690876352726703e+19 ( -2.46 % )
	Average time between blocks in last day: 9.46 min
	Average time between blocks in last week: 10.08 min
	Average time between blocks in last month: 9.35 min

	Total Coins Mined: 17,830,425
	Current Reward: 12.5
	Blocks Until Next Halving: 43,566 ( ~303 days )

	Price: $10,572.54 ( 1.58 % )
	Market Cap: $188,512,881,530

	Historical Prices:
	2018-07-21 :  $7,419.29      42.50 %
	2017-07-21 :  $2,667.76     296.31 %
	2016-07-21 :    $665.01    1489.83 %
	2015-07-21 :    $275.83    3732.99 %
	2014-07-21 :    $622.21    1599.19 %


### Set Up Instructions:

- Run a full Bitcoin node. https://bitcoincore.org/

- Install the alerter. This will create a database of block info.
```
./main.py --install
```

- *Optional* Import Historical Price Data.
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

- Edit the default config.json that was created automatically during the install. Format:
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
"use_regtest": true, 
"minutes_to_sleep": 5, 
"status_frequency_in_hours": 0, 
"historical_price_filename": "daily_history.csv", 
"catch_errors": false, 
"block_reorg_threshold": 0, 
"minutes_between_blocks_threshold": 90, 
"price_percent_change_threshold": 5, 
"reorg_depth_cap": 5
}
```

- Start the Bitcoin Alerter
```
./main.py --run
```
