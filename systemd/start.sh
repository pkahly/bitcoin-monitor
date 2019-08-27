#!/bin/bash

bitcoind -datadir=<DATA DIR>&

sleep 600

cd /home/<USER>/bitcoin-monitor
./main.py --run
