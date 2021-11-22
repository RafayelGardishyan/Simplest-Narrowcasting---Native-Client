#!/bin/bash

sudo apt update
sudo apt install python3-pyqt5

pip3 install -r requirements.txt

xterm -e python3 text_loader.py 
xterm -e python3 main.py 
