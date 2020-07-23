from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5 import QtGui, QtCore
from threading import Thread
from collections import deque
import time
import cv2
import UI.resources_rc

class CameraWidget(QWidget):
    def __init__(self, width, height, stream_link=0, parent=None, deque_size=1):
        super(CameraWidget, self).__init__(parent)
        self.deque = deque(maxlen=deque_size)
        self.screen_width = width
        self.screen_height = height
        self.camera_stream_link = stream_link
        self.online = False
        self.capture = None
        self.video_frame = QLabel()
        self.load_network_stream()
        self.get_frame_thread = Thread(target=self.get_frame, args=())
        self.get_frame_thread.daemon = True
        self.get_frame_thread.start()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.set_frame)
        self.timer.start(.5)

    def load_network_stream(self):
        def load_network_stream_thread():
            if self.camera_stream_link == None:
                self.capture = cv2.VideoCapture(self.camera_stream_link)
                self.online = True
            elif self.verify_network_stream(self.camera_stream_link):
                self.capture = cv2.VideoCapture(self.camera_stream_link)
                self.online = True
        self.load_stream_thread = Thread(target=load_network_stream_thread, args=())
        self.load_stream_thread.daemon = True
        self.load_stream_thread.start()

    def verify_network_stream(self, link):
        cap = cv2.VideoCapture(link)
        if not cap.isOpened():
            return False
        cap.release()
        return True

    def get_frame(self):
        while True:
            try:
                if(self.online and (self.camera_stream_link == None)):
                    image = cv2.imread("UI/resources/STATIC.png")
                    self.deque.append(image)

                elif self.capture.isOpened() and self.online:
                    status, frame = self.capture.read()
                    if status:
                        self.deque.append(frame)
                    else:
                        self.capture.release()
                        self.online = False
                else:
                    #print('attempting to reconnect', self.camera_stream_link)
                    self.load_network_stream()
                    image = cv2.imread("UI/resources/STATIC.png")
                    self.deque.append(image)
                    frame = self.deque[-1]
                    self.frame = cv2.resize(frame, (self.screen_width, self.screen_height))
                    self.img = QtGui.QImage(self.frame, self.frame.shape[1], self.frame.shape[0],QtGui.QImage.Format_RGB888).rgbSwapped()
                    self.pix = QtGui.QPixmap.fromImage(self.img)
                    self.video_frame.setPixmap(self.pix)
                    self.spin(2)
                self.spin(.001)
            except AttributeError:
                pass

    def spin(self, seconds):
        time_end = time.time() + seconds
        while time.time() < time_end:
            QApplication.processEvents()

    def set_frame(self):
        if not self.online:
            self.spin(1)
            return
        if self.deque and self.online:
            frame = self.deque[-1]
            self.frame = cv2.resize(frame, (self.screen_width, self.screen_height))
            self.img = QtGui.QImage(self.frame, self.frame.shape[1], self.frame.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
            self.pix = QtGui.QPixmap.fromImage(self.img)
            self.video_frame.setPixmap(self.pix)

    def get_video_frame(self):
        return self.video_frame

    def change_stream(self, stream):
        self.camera_stream_link = stream
        self.online = False