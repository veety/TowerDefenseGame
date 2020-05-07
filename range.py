from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGraphicsPixmapItem

class Range(QGraphicsPixmapItem):
    def __init__(self,x,y,range):
        super(QGraphicsPixmapItem, self).__init__()
        self.square_size=40
        self.pixmap=QPixmap()
        self.pixmap.load("gui/range.png")
        self.pixmap=self.pixmap.scaled(range*2, range*2)
        self.setPixmap(self.pixmap)
        self.setX(self.square_size * x -range +self.square_size/2)
        self.setY(self.square_size * y -range +self.square_size/2)