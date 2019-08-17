#### Note: Still under construction -- needs productionized, automated tests, etc. See open issues.

*Developed primarily for my own use, but feedback and contributions are welcome*

## Monitors a full Bitcoin node and sends status emails and alerts.

### Sample alerts:
```
TODO
```

### Sample status update:
```

```

### Sample daily summary:
```

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
