import os
import requests
import json
from time import sleep

while True:
    if not os.path.isfile("data/READING.hey"):
        print("Getting text data")
        id = 1
        with open("data/WRITING.hey", 'wb') as w:
            w.close()

        with open("data/screen.id", 'r') as si:
            id = int(si.read())
            si.close()
        
        try:
            url = "https://pgtv.pythonanywhere.com/internal/get_text_data/{}".format(id)
            r = requests.get(url)
            if r.status_code != 200:
                print("Screen: Could not load next slide")

            with open("data/data.txt", 'wb') as dat:
                dat.write(json.dumps(r.json()).encode())
        except Exception as e:
            print("Whoops!", e)

        os.remove("data/WRITING.hey")
        sleep(20)
    sleep(1)
            