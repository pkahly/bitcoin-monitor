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


### Instructions:

- Run a full Bitcoin node (find instructions elsewhere)

- Run install/install.py to create a new sqllite3 database
   Can run install/uninstall.py to drop the database tables and allow rerunning install/install.py

- Run install/add_price_data.py to import historical price data 
   daily_history.csv must exist in the root directory in the correct format

- Run install/add_blocks.py to save block hashes for reorg detection
   This is optional as full_node_monitor.py will do the same thing during it's first run

- Create config.json. Format:
```
{
"SERVER": <server>,
"PORT": <port>,
"BOT_EMAIL": <email>,
"BOT_PASSWORD": <pass>,
"HUMAN_EMAIL": <your email>
}
```

- Run full_node_monitor.py
   This is the main loop
   This will read and write the database tables created earlier
