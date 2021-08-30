#!/bin/bash

sudo apt update
sudo apt install python3-pyqt5

pip3 install -r requirements.txt
python3 main.py
