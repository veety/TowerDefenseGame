from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import *
from enemy import *
from math import *
from math import sqrt, pow, fabs
from PyQt5.QtWidgets import QGraphicsPixmapItem

class Projectile(QtWidgets.QGraphicsPixmapItem):

    def __init__(self, target, x, y):
        super(Projectile, self).__init__()
        self.x=x
        self.y=y
        self.target=target
        self.speed=20
        self.square_size=40
        self.ticks=50
        self.pixmap=QBitmap()
        self.pixmap.load("items/projectile.png")
        self.setPixmap(self.pixmap)
        self.finished=False
        self.setX(self.x)
        self.setY(self.y)
        self.updateAll()

    def updateAll(self):
        self.updatePosition()
        self.updateRotation()

    def updatePosition(self):
        dX = self.target.get_x() - self.x
        dY = self.target.get_y() - self.y
        unitX = dX / (sqrt(pow(dX, 2)+pow(dY, 2)))
        unitY = dY / (sqrt(pow(dX, 2) + pow(dY, 2)))
        self.x = self.x + self.speed * unitX
        self.y =self.y + self.speed * unitY
        self.setX(self.x)
        self.setY(self.y)
        if fabs(self.x-self.target.get_x()+self.y-self.target.get_y())<=self.speed/2:
            self.finished=True

    def updateRotation(self):
        try:
            deltay = self.target.position_y - self.y
            deltax = self.target.position_x - self.x
            if deltax >= 0:
                if deltax == 0:
                    if deltay < 0:
                        rotation = 0
                    else:
                        rotation = 180
                else:
                    rotation = atan((deltay) / (deltax)) * 180 / pi + 90
            else:
                if deltax == 0:
                    if deltay < 0:
                        rotation = 0
                    else:
                        rotation = 180
                else:
                    rotation = atan((deltay / deltax)) * 180 / pi - 90
            self.setRotation(rotation)
        except:
            pass