from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QListWidget, QSpacerItem, QSizePolicy
from PyQt5 import QtGui, QtCore
from UI.DistanceUI import Ui_MainWindow
from camera import CameraWidget

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.exitButton.clicked.connect(self.onClose)
        self.camera_list = []
        self.onStart()
        self.listWidget.currentRowChanged.connect(self.changeStream)
        #self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        #self.showFullScreen()
        self.displayTime()
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.displayTime)
        self.timer.start()

    def onClose(self):
        self.close()

    def onStart(self):
        file = open("Distance_Stream.txt", "r")
        data = file.read()
        data = data.split("\n")
        for item in data:
            item = item.split(",")
            self.camera_list.append(item)

        for item in self.camera_list:
            self.listWidget.addItem(item[0])

    def changeStream(self, i):
        self.videoStream.change_stream(self.camera_list[i][1])


    def displayTime(self):
        self.dateQLabel.setText(QtCore.QDate.currentDate().toString())
        self.timeQLabel.setText(QtCore.QTime.currentTime().toString())

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
