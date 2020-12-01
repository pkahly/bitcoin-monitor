#!/usr/bin/python3

import argparse
from lib import bitcoin_alerter, install, debug, watchlist, config_reader
import logging
import sys

## Set Up File and STDOUT Logging
logging.root.handlers = []
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s \t  %(message)s",
    handlers=[
        logging.FileHandler("bitcoin-monitor.log", mode='a'),
        logging.StreamHandler(sys.stdout)
    ]
)


## Argument Parsing ##
parser = argparse.ArgumentParser(description='Tools for sending status and alerts for a full Bitcoin node')

parser.add_argument('--run',
                       action='store_true',
                       help='run the alerter')
parser.add_argument('--run_daily_summary',
                       action='store_true',
                       help='run the alerter\'s daily summary')

parser.add_argument('--install',
                       action='store_true',
                       help='create the database and populate with block info')
parser.add_argument('--import_price_history',
                       action='store',
                       type=str,
                       metavar='FILENAME',
                       help='populate database with historical prices')
parser.add_argument('--uninstall',
                       action='store_true',
                       help='dump the database tables')

parser.add_argument('--watchlist_old_utxo',
                       action='store',
                       type=int,
                       metavar='BLOCK_HEIGHT',
                       help='add utxo which originated before BLOCK_HEIGHT to the watchlist')  
parser.add_argument('--check_watchlist',
                       action='store_true',
                       help='check watchlisted utxo against utxo set')
parser.add_argument('--clear_watchlist',
                       action='store_true',
                       help='delete all utxo from watchlist')

parser.add_argument('--print_blocks',
                       action='store_true',
                       help='Print the contents of the blocks database')
parser.add_argument('--print_price_history',
                       action='store_true',
                       help='Print the contents of the price database')
parser.add_argument('--print_status_history',
                       action='store_true',
                       help='Print the contents of the status database')                                                                     


# Load config (this should be the ONLY config load)
config = config_reader.load_config()

# Process flags
args = parser.parse_args()

if args.install:
   install.install()
   install.add_blocks(config)

elif args.import_price_history:
   install.import_historical_prices(args.import_price_history)

elif args.uninstall:
   install.uninstall()

elif args.run:
   bitcoin_alerter.run_bitcoin_alerter(config)
   
elif args.run_daily_summary:
   bitcoin_alerter.send_daily_summary(config)

elif args.watchlist_old_utxo:
   watchlist.add_old_utxo(args.watchlist_old_utxo)

elif args.check_watchlist:
   watchlist.check_watchlist(config)
   
elif args.clear_watchlist:
   watchlist.clear_watchlist()
   
elif args.print_blocks:
   debug.print_blocks()

elif args.print_price_history:
   debug.print_price_history()

elif args.print_status_history:
   debug.print_status_history()
else:
   print("Use '--help' to see options")
