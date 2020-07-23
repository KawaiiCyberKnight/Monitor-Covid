from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QSpacerItem, QSizePolicy, QGridLayout, QLabel, QListWidgetItem
from PyQt5 import QtGui, QtCore
from UI.FeverUI import Ui_MainWindow
from camera import CameraWidget
from card import CardWidget

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.exitButton.clicked.connect(self.onClose)
        self.camera_list = []
        self.onStart()
        self.sideupperSelection.itemSelectionChanged.connect(self.changeStreamUpper)
        self.mainSelection.itemSelectionChanged.connect(self.changeStreamMain)
        self.sidelowerSelection.itemSelectionChanged.connect(self.changeStreamLower)
        #self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        #self.showFullScreen()
        self.displayTime()
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.displayTime)
        self.timer.start()

    #def keyPressEvent(self, event):
        #print(event)
        #customItem = CardWidget("","","100","200")
        #customListItem = QListWidgetItem(self.warningList)
        #customListItem.setSizeHint(customItem.sizeHint())
        #self.warningList.addItem(customListItem)
        #self.warningList.setItemWidget(customListItem, customItem)

    def onClose(self):
        self.close()

    def onStart(self):
        file = open("Fever_Stream.txt", "r")
        data = file.read()
        data = data.split("\n")
        for item in data:
            item = item.split(",")
            name, dir = item
            self.camera_list.append([name, dir, 0])
        #Main Stream 1
        #Upper Stream 2
        #Lower Stream 3
        for item in self.camera_list:
            self.sideupperSelection.addItem(item[0])
            self.mainSelection.addItem(item[0])
            self.sidelowerSelection.addItem(item[0])

    def changeStreamMain(self):
        i = self.mainSelection.currentRow()
        x=0
        for item in self.camera_list:
           if item[2]==1:
               self.camera_list[x][2] = 0
           x+=1
        if self.camera_list[i][2] == 2:
            self.sideupperSelection.clearSelection()
            self.sideupperStream.change_stream(None)
        elif self.camera_list[i][2] == 3:
            self.sidelowerSelection.clearSelection()
            self.sidelowerStream.change_stream(None)
        self.camera_list[i][2] = 1
        self.mainStream.change_stream(self.camera_list[i][1])
        print(self.camera_list)

    def changeStreamUpper(self):
        i = self.sideupperSelection.currentRow()
        x = 0
        for item in self.camera_list:
            if item[2] == 2:
                self.camera_list[x][2] = 0
            x += 1
        if self.camera_list[i][2] == 1:
            self.mainSelection.clearSelection()
            self.mainStream.change_stream(None)
        elif self.camera_list[i][2] == 3:
            self.sidelowerSelection.clearSelection()
            self.sidelowerStream.change_stream(None)
        self.camera_list[i][2] = 2
        self.sideupperStream.change_stream(self.camera_list[i][1])
        print(self.camera_list)

    def changeStreamLower(self):
        i = self.sidelowerSelection.currentRow()
        x = 0
        for item in self.camera_list:
            if item[2] == 3:
                self.camera_list[x][2] = 0
            x += 1
        if self.camera_list[i][2] == 1:
            self.mainSelection.clearSelection()
            self.mainStream.change_stream(None)
        elif self.camera_list[i][2] == 2:
            self.sideupperSelection.clearSelection()
            self.sideupperStream.change_stream(None)
        self.camera_list[i][2] = 3
        self.sidelowerStream.change_stream(self.camera_list[i][1])
        print(self.camera_list)


    def displayTime(self):
        self.dateQLabel.setText(QtCore.QDate.currentDate().toString())
        self.timeQLabel.setText(QtCore.QTime.currentTime().toString())

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
