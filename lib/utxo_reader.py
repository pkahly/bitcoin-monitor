
# Provides an iterator to read UTXO info from a CSV file
# This file can be generated using a variety of tools
# One such tool: https://github.com/in3rsha/bitcoin-utxo-dump
# Use command 'utxodump  -f count,txid,vout,height,coinbase,amount,script,type,address'


# Usage:
# for utxo in UtxoIterator():
#    print(utxo)


# Reads UTXO info from this file:
UTXO_FILE = "utxo.csv"

class UtxoIterator:
   def __init__(self):
      self.file = open(UTXO_FILE, 'r')
      self.keys = self._get_split_line()

   def __next__(self):
      line_split = self._get_split_line()
      if len(line_split) < len(self.keys):
         raise StopIteration
      
      # Add values to dictionary, with csv headings as keys
      utxo = {}
      for index in range(0, len(line_split)):
         utxo[self.keys[index]] = line_split[index]
      
      return utxo

   def __iter__(self):
      return self
      
   def _get_split_line(self):
      line = self.file.readline().replace('\n', '')
      return line.split(',')
