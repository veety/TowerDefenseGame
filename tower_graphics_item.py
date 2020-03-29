from PyQt5 import QtWidgets, QtGui, QtCore
from globals import squareSize
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from math import *
from enemy import *

class TowerGraphicsItem(QtWidgets.QGraphicsPolygonItem):

    def __init__(self,tower,gui):
        super(TowerGraphicsItem, self).__init__()
        self.gui=gui
        self.tower=tower
        self.square_size=squareSize
        self.selected=False
        brush = QtGui.QBrush(1)
        self.setBrush(brush)
        self.drawRange=False
        self.constructTriangleVertices()
        self.setX(self.tower.position_x - squareSize / 2)
        self.setY(self.tower.position_y - squareSize / 2)
        self.updateRotation()

    def mousePressEvent(self, event):
        if self.tower.is_purchasable==True and self.gui.tower_selected==None:
            self.gui.tower_selected=self.tower
        if not self.tower.is_purchasable:
            self.drawRange=True



    def constructTriangleVertices(self):
        triangle = QtGui.QPolygonF()
        triangle.append(QtCore.QPointF(self.square_size / 2, 0))
        triangle.append(QtCore.QPointF(0, self.square_size))
        triangle.append(QtCore.QPointF(self.square_size, self.square_size))
        triangle.append(QtCore.QPointF(self.square_size / 2, 0))
        self.setPolygon(triangle)
        self.setTransformOriginPoint(self.square_size / 2, self.square_size / 2)

    def updateRotation(self):
        try:
            deltay=self.tower.current_target.position_y-self.tower.position_y
            deltax=self.tower.current_target.position_x-self.tower.position_x
            if deltax>=0:
                if deltax==0:
                    if deltay<0:
                        rotation=0
                    else:
                        rotation=180
                else:
                    rotation=atan((deltay)/(deltax))*180/pi+90
            else:
                if deltax == 0:
                    if deltay < 0:
                        rotation = 0
                    else:
                        rotation = 180
                else:
                    rotation=atan((deltay/deltax))*180/pi-90
            self.setRotation(rotation)
        except:
            pass