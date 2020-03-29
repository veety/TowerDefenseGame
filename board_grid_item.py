from PyQt5 import QtWidgets, QtGui, QtCore
from globals import squareSize
from PyQt5.QtGui import QColor, QBrush
from coordinates import *
from tower import *

class BoardGridItem(QtWidgets.QGraphicsPolygonItem):

    def __init__(self,x,y,ispath,gui):
        super(BoardGridItem, self).__init__()
        self.gui=gui
        self.x=x
        self.y=y
        self.square_size=squareSize
        self.ispath=ispath
        if ispath:
            brush = QtGui.QBrush(QColor(150, 75, 0))
        else:
            brush = QBrush(QColor(30, 130, 30))
        self.setBrush(brush)
        self.constructSquareVertices()
        self.setX(x*squareSize)
        self.setY(y*squareSize)

    def mousePressEvent(self, event):
        if self.gui.tower_selected!=None and not self.ispath:
            tower=Tower()
            self.gui.board.add_tower(tower,Coordinates(self.x,self.y))
            self.gui.tower_selected=None
        else:
            self.gui.tower_selected=None

    def constructSquareVertices(self):
        square = QtGui.QPolygonF()
        square.append(QtCore.QPointF(0, 0))
        square.append(QtCore.QPointF(0, self.square_size))
        square.append(QtCore.QPointF(self.square_size, self.square_size))
        square.append(QtCore.QPointF(self.square_size, 0))
        self.setPolygon(square)
        self.setTransformOriginPoint(self.square_size / 2, self.square_size / 2)