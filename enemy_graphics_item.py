from PyQt5 import QtWidgets, QtGui, QtCore
from globals import squareSize

class EnemyGraphicsItem(QtWidgets.QGraphicsPolygonItem):

    def __init__(self,enemy):
        super(EnemyGraphicsItem, self).__init__()
        self.enemy=enemy
        self.square_size=squareSize
        brush = QtGui.QBrush(1)
        self.setBrush(brush)
        self.constructTriangleVertices()
        self.updateAll()

    def constructTriangleVertices(self):
        triangle = QtGui.QPolygonF()
        triangle.append(QtCore.QPointF(self.square_size / 2, 0))
        triangle.append(QtCore.QPointF(0, self.square_size))
        triangle.append(QtCore.QPointF(self.square_size, self.square_size))
        triangle.append(QtCore.QPointF(self.square_size / 2, 0))
        self.setPolygon(triangle)
        self.setTransformOriginPoint(self.square_size / 2, self.square_size / 2)

    def updateAll(self):
        self.updatePosition()
        self.updateRotation()

    def updatePosition(self):
        self.setX(self.enemy.position_x-squareSize/2)
        self.setY(self.enemy.position_y-squareSize/2)

    def updateRotation(self):
        if self.enemy.get_direction()=='RIGHT':
            self.setRotation(90)
        if self.enemy.get_direction()=='UP':
            self.setRotation(0)
        if self.enemy.get_direction()=='LEFT':
            self.setRotation(270)
        if self.enemy.get_direction()=='DOWN':
            self.setRotation(180)