#!/bin/bash

sudo apt update
sudo apt install python3-pyqt5

pip3 install -r requirements.txt

lxterminal -e python3 text_loader.py 
lxterminal -e python3 main.py 
