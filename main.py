#!/usr/bin/python3

from lib import bitcoin_alerter, install


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
      print("1. Print ....")
      
      choice = int(input("> "))

      if choice == 1:
         print()
      elif choice == 2:
         install_menu()     
      elif choice == 3:
         debug_menu()
      else:
         return


##############################################################


while True:
   print()
   print("Welcome to the Bitcoin-Alerter")
   print("1. Run the Bitcoin Alerter")
   print("2. Installation Options")
   print("3. Debugging Options")
   print("4. Exit")

   choice = int(input("> "))

   if choice == 1:
      print("Running Alerter...")
      #bitcoin_alerter.run_bitcoin_alerter_with_exponential_backoff()
   elif choice == 2:
      install_menu()     
   elif choice == 3:
      debug_menu()
   else:
      exit()
