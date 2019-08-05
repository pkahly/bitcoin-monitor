#!/usr/bin/python3

import argparse
from lib import bitcoin_alerter, install, debug


def install_menu():
   while True:
      print()
      print("1. Install Alerter")
      print("2. Import Historical Price Data")
      print("3. Store Block Info")
      print("4. Uninstall Alerter")
      print("5. Back")
      
      choice = int(input("> "))

      if choice == 1:
         install.install()
      elif choice == 2:
         install.import_historical_prices()
      elif choice == 3:
         install.add_blocks()
      elif choice == 4:
         install.uninstall()
      else:
         return


def debug_menu():
   while True:
      print()
      print("1. Print Blocks")
      print("2. Print Price History")
      print("3. Print Status History")
      print("4. Back")
      
      choice = int(input("> "))

      if choice == 1:
         debug.print_blocks()
      elif choice == 2:
         debug.print_price_history()    
      elif choice == 3:
         debug.print_status_history()
      else:
         return
         
         
def main_menu():
   while True:
      print()
      print("Welcome to the Bitcoin-Alerter")
      print("1. Run the Bitcoin Alerter")
      print("2. Installation Options")
      print("3. Configuration")
      print("4. Debugging")
      print("5. Administration")
      print("6. Exit")

      choice = int(input("> "))

      if choice == 1:
         print("Running Alerter...")
         bitcoin_alerter.run_bitcoin_alerter()
      elif choice == 2:
         install_menu()
      elif choice == 3:
         print("Not implemented")
      elif choice == 4:
         debug_menu()
      elif choice == 5:
         print("Not implemented")
      else:
         exit()


##############################################################


parser = argparse.ArgumentParser(description='Tools for sending status and alerts for a full Bitcoin node')
parser.add_argument('--run',
                       action='store_true',
                       help='run the alerter (skip menu)')
parser.add_argument('--install',
                       action='store_true',
                       help='run install scripts (skip menu)')
args = parser.parse_args()

if args.install:
   install.install()
   install.import_historical_prices()
   install.add_blocks()
elif args.run:
   bitcoin_alerter.run_bitcoin_alerter()
else:
   main_menu()
