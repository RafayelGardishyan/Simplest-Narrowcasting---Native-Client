#!/bin/bash

sudo apt update
sudo apt install python3-pyqt5

pip3 install -r requirements.txt

sh python3 text_loader.py &  PIDT=$!
sh python3 main.py &  PIDS=$!
wait $PIDT
wait $PIDS