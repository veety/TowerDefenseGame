from PyQt5 import QtWidgets
from PyQt5.QtGui import *

class EnemyGraphicsItem(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, gui, enemy):
        super().__init__()
        self.gui=gui
        self.enemy = enemy
        self.fullHealth=str(self.enemy.health)
        self.enemy.graphicsItem = self
        self.square_size = 40
        self.setTransformOriginPoint(self.square_size / 2, self.square_size / 2)
        self.updateAll()

    def updateAll(self):
        self.updatePosition()
        self.updateRotation()

    def updatePosition(self):
        self.setX(self.enemy.position_x - self.square_size / 2)
        self.setY(self.enemy.position_y - self.square_size / 2)

    def updateRotation(self):
        if self.enemy.get_direction() == 'RIGHT':
            self.setRotation(90)
        if self.enemy.get_direction() == 'UP':
            self.setRotation(0)
        if self.enemy.get_direction() == 'LEFT':
            self.setRotation(270)
        if self.enemy.get_direction() == 'DOWN':
                self.setRotation(180)

class EnemyGraphicsItemA(EnemyGraphicsItem):
    def __init__(self, gui, enemy):
        super().__init__(gui, enemy)
        self.pixmap=QPixmap()
        self.pixmap.load("items/enemy_a.png")
        self.setPixmap(self.pixmap)

class EnemyGraphicsItemB(EnemyGraphicsItem):
    def __init__(self, gui, enemy):
        super().__init__(gui, enemy)
        self.pixmap=QPixmap()
        self.pixmap.load("items/enemy_b.png")
        self.setPixmap(self.pixmap)

class EnemyGraphicsItemC(EnemyGraphicsItem):
    def __init__(self, gui, enemy):
        super().__init__(gui, enemy)
        self.pixmap=QPixmap()
        self.pixmap.load("items/enemy_c.png")
        self.setPixmap(self.pixmap)
