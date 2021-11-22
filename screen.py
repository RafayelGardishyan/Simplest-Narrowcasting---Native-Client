from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
import json
import requests

class Screen(QWidget):
    def __init__(self, pin):
        super().__init__()
    
        self.pin = pin

        print("Screen: Initializing")

        self.playlist = []
        self.ppointer = 0

        self.setWindowTitle("PG TV - Screen {}".format(self.pin))

        self.topTitle = QLabel("PG TV")
        self.topTitle.setFont(QFont('Bungee', 32))
        self.topTitle.setAlignment(Qt.AlignLeft)
        self.topTitle.setStyleSheet("color: #fff; margin-left: 100px;")
        # self.topTitle.clicked.connect(lambda: self.close())

        self.topInfo = QLabel("[Time | Weather]")
        self.topInfo.setFont(QFont("Bungee", 32))
        self.topInfo.setAlignment(Qt.AlignRight)
        self.topInfo.setStyleSheet("color: #ffd752; margin-right: 100px;")

        topContainer = QHBoxLayout()
        topContainer.addWidget(self.topTitle)
        topContainer.addWidget(self.topInfo)

        self.contentImage = QLabel()
        self.contentImage.setPixmap(self.get_pixmap("img/placeholder.jpg"))
        self.contentImage.setAlignment(Qt.AlignCenter)

        self.lowerText = QLabel("Lower Text")
        self.lowerText.setFont(QFont('Bungee', 32))
        self.lowerText.setAlignment(Qt.AlignCenter)

        mainContainer = QVBoxLayout()

        mainContainer.addLayout(topContainer)
        mainContainer.addWidget(self.contentImage)
        mainContainer.addWidget(self.lowerText)

        self.setLayout(mainContainer)


        
        self.load_screen()
        self.load_playlist()
        self.next_image()
        # self.load_image()

    def show(self):
        super().showFullScreen()
        print("Screen: Showing")

    def get_pixmap(self, file):
        contentPixmap = QPixmap(file)
        return contentPixmap.scaled(1400, 787, QtCore.Qt.KeepAspectRatio)

    def load_playlist(self):
        print("Loading playlist")
        try:
            url = "https://pgtv.pythonanywhere.com/internal/get_playlist/{}".format(self.id)
            r = requests.get(url)
            if r.status_code != 200:
                print("Screen: Could not load playlist")

            new_playlist = []

            for slide in r.json():
                image = requests.get("https://pgtv.pythonanywhere.com" + slide)
                
                if not os.path.isfile("img/" + slide[17:]):            
                    with open("img/" + slide[17:], 'wb') as img:
                        img.write(image.content)
                        img.close()

                new_playlist.append(slide[17:])

            self.playlist = new_playlist

        except Exception as e:
            print("Error: {}; trying again".format(e))

    def next_image(self):
        if len(self.playlist) == 0:
            return

        self.contentImage.setPixmap(self.get_pixmap("img/" + self.playlist[self.ppointer]))
        self.ppointer += 1

    def load_text(self):
        if not os.path.isfile("data/WRITING.hey"):
            with open("data/READING.hey", 'wb') as w:
                w.close()

            with open("data/data.txt", 'r') as dat:
                text = json.loads(dat.read())
                dat.close()

            self.lowerText.setText(text["sctext"])

            print("Screen: New image loaded")

            self.topInfo.setText("[ {} | {}° ]".format(text["time"], text["weather"]["temp"]))
            self.setStyleSheet("background-color: {};".format(text["screen"][0]["fields"]["background_color"]))
            self.lowerText.setStyleSheet("color: {};".format(text["screen"][0]["fields"]["content_border_color"]))
            self.topInfo.setStyleSheet("color: {}; margin-right: 100px;".format(text["screen"][0]["fields"]["content_border_color"]))

            print("Screen: New styles applied")

            os.remove("data/READING.hey")


    def load_screen(self):
        url = "https://pgtv.pythonanywhere.com/internal/get_metadata/{}".format(self.pin)
        r = requests.get(url)
        if r.status_code != 200:
            print("Screen: Could not load screen data")

        self.data = r.json()

        self.lowerText.setText(self.data[0]["fields"]["scroll_text"])
        self.setStyleSheet("background-color: {};".format(self.data[0]["fields"]["background_color"]))
        self.contentImage.setStyleSheet(
            "margin-left: 75px; margin-right: 75px; border-color: {}".format(
                self.data[0]["fields"]["content_border_color"]
            )
        )
        self.lowerText.setStyleSheet("color: {};".format(self.data[0]["fields"]["content_border_color"]))

        self.id = self.data[0]["pk"]

        with open("data/screen.id", 'w') as si:
            si.write(str(self.id))
            si.close()

        self.itimer = QtCore.QTimer()
        self.itimer.timeout.connect(self.next_image)
        self.itimer.start(self.data[0]["fields"]["time"])

        self.ttimer = QtCore.QTimer()
        self.ttimer.timeout.connect(self.load_text)
        self.ttimer.start(20000)

        self.ptimer = QtCore.QTimer()
        self.ptimer.timeout.connect(self.load_playlist)
        self.ptimer.start(20 * 60 * 1000)


