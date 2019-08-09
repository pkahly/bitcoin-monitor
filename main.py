#!/usr/bin/python3

import argparse
from lib import bitcoin_alerter, install, debug


parser = argparse.ArgumentParser(description='Tools for sending status and alerts for a full Bitcoin node')

parser.add_argument('--run',
                       action='store_true',
                       help='run the alerter')
parser.add_argument('--install',
                       action='store_true',
                       help='create the database and populate with historical prices and blocks')
parser.add_argument('--uninstall',
                       action='store_true',
                       help='dump the database tables')                       
parser.add_argument('--print_blocks',
                       action='store_true',
                       help='Print the contents of the blocks database')
parser.add_argument('--print_price_history',
                       action='store_true',
                       help='Print the contents of the price database')
parser.add_argument('--print_status_history',
                       action='store_true',
                       help='Print the contents of the status database')                                                                     

args = parser.parse_args()


if args.install:
   install.install()
   install.import_historical_prices()
   install.add_blocks()
elif args.uninstall:
   install.uninstall()
elif args.run:
   bitcoin_alerter.run_bitcoin_alerter()
elif args.print_blocks:
   debug.print_blocks()
elif args.print_price_history:
   debug.print_price_history()
elif args.print_status_history:
   debug.print_status_history()
else:
   print("Use '--help' to see options")
