#!/usr/bin/python3

import time
import subprocess

# Simulates mining by generating regtest blocks at a set rate #

BLOCK_TIME = 30
SAMPLE_WALLET = "2N1fyHrryDd7KqRapaiokFnWr6K9yFH3bDp"

while True:
   print(subprocess.check_output(["bitcoin-cli", "-regtest", "generatetoaddress", "1", wallet]))
   time.sleep(BLOCK_TIME)
