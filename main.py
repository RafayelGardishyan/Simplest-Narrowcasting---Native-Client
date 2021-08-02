from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from screen import Screen

class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PG TV - Raspi Client")

        centralWidget = QWidget()

        mainContainer = QVBoxLayout()

        l = QLabel("PG TV - Scherm")
        l.setFont(QFont('Bungee', 24))
        mainContainer.addWidget(l)

        self.pinInput = QLineEdit()
        self.pinInput.setFont(QFont('Bungee', 8))

        self.loginButton = QPushButton("Log in")
        self.loginButton.setFont(QFont('Bungee', 8))
        self.loginButton.clicked.connect(self.loadScreen)

        pinContainer = QHBoxLayout()
        p = QLabel("Pin:")
        p.setFont(QFont('Bungee', 12))
        pinContainer.addWidget(p)
        pinContainer.addWidget(self.pinInput)

        mainContainer.addLayout(pinContainer)
        mainContainer.addWidget(self.loginButton)

        centralWidget.setLayout(mainContainer)
        centralWidget.setStyleSheet("background-color: #ffd752;")

        self.setCentralWidget(centralWidget)
    
    def loadScreen(self):
        if self.screen != None:
            self.screen = Screen(self.pinInput.text())
        self.screen.show()


app = QApplication([])


startWindow = StartWindow()

startWindow.show()

app.exec_()