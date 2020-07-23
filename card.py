from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5 import QtGui

class CardWidget(QWidget):
    def __init__ (self, rgbIcon, thermalIcon, temp, time, parent=None):
        super(CardWidget, self).__init__(parent)
        self.rgbIcon = rgbIcon
        self.thermalIcon = thermalIcon
        self.temp = temp
        self.time = time
        self.setup()

    def setup(self):
        self.MainQHBoxLayout = QHBoxLayout()
        self.rgbIconLabel = QLabel()
        self.thermalIconLabel = QLabel()
        self.tempLabel = QLabel()
        self.timeLabel = QLabel()

        #self.rgbIconLabel.setPixmap(self.rgbIcon)
        #self.thermalIconLabel.setPixmap(self.thermalIcon)
        self.tempLabel.setText(self.temp)
        self.timeLabel.setText(self.time)

        self.MainQHBoxLayout.addWidget(self.rgbIconLabel)
        self.MainQHBoxLayout.addWidget(self.thermalIconLabel)
        self.MainQHBoxLayout.addWidget(self.tempLabel)
        self.MainQHBoxLayout.addWidget(self.timeLabel)
        self.setLayout(self.MainQHBoxLayout)