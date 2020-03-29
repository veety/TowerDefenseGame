from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import *
from board import *
from tower import *
from globals import *
from coordinates import Coordinates
from enemy_graphics_item import *
from tower_graphics_item import TowerGraphicsItem
from board_grid_item import *
import timer

class GUI(QtWidgets.QMainWindow):
    def __init__(self,board,square_size):
        super().__init__()
        self.setCentralWidget(QtWidgets.QWidget())
        self.horizontal=QtWidgets.QHBoxLayout()
        self.centralWidget().setLayout(self.horizontal)
        self.board=board
        self.board.gui=self
        self.timer=None
        self.enemies=[]
        self.towers=[]
        self.square_size=square_size
        self.init_window()
        self.add_board_grid_items()
        self.update_enemies()
        self.tower_selected=None
        self.tower1=Tower()
        self.tower1.is_purchasable=True
        self.tower1.position_x = squareSize * boardWidth + squareSize
        self.tower1.position_y = squareSize
        self.tower1item=TowerGraphicsItem(self.tower1,self)
        self.scene.addItem(self.tower1item)

    def add_board_grid_items(self):
        for i in range(self.board.get_width()):
            for j in range(self.board.get_height()):
                coordinates=Coordinates(i,j)
                ispath=self.board.get_square(coordinates).is_path()
                if ispath:
                    rectangle=BoardGridItem(i,j,True,self)
                   # qp = QBrush(QColor(150, 75, 0), Qt.SolidPattern)
                   # rectangle = QGraphicsRectItem(self.square_size * coordinates.get_x(),
                   #                               self.square_size * coordinates.get_y(), self.square_size,
                   #                               self.square_size)
                   # rectangle.setBrush(qp)
                else:
                    rectangle=BoardGridItem(i,j,False,self)
                   # qp = QBrush(QColor(30, 130, 30), Qt.SolidPattern)
                   # rectangle = QGraphicsRectItem(self.square_size * coordinates.get_x(),
                   #                               self.square_size * coordinates.get_y(), self.square_size,
                   #                               self.square_size)
                   # rectangle.setBrush(qp)
                self.scene.addItem(rectangle)

    def init_window(self):
        self.setGeometry(300,300,800,800)
        self.setWindowTitle('Tower Defense')
        self.show()

        self.scene=QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0,0,600,600)

    #    self.t=QtWidgets.QGraphicsScene()
     #   self.t.setSceneRect(0,0,300,300)

        #self.viewt = QtWidgets.QGraphicsView(self.t, self)
     #   self.viewt.adjustSize()
     #   self.viewt.show()
     #   self.horizontal.addWidget(self.viewt)

        self.view=QtWidgets.QGraphicsView(self.scene,self)
        self.view.adjustSize()
        self.view.show()
        self.horizontal.addWidget(self.view)

    def get_enemy_graphics_items(self):
        items=[]
        for item in self.scene.items():
            if type(item) is EnemyGraphicsItem:
                items.append(item)
        return items

    def get_tower_graphics_items(self):
        items=[]
        for item in self.scene.items():
            if type(item) is TowerGraphicsItem:
                items.append(item)
        return items

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_P:
            self.board.timer.pause()

    def update_towers(self):
        if self.towers < self.board.towers:
            tower=TowerGraphicsItem(self.board.towers[-1],self)
            self.towers.append(self.board.towers[-1])
            self.scene.addItem(tower)
        for tower_item in self.get_tower_graphics_items():
            tower_item.updateRotation()

    def update_enemies(self):
        if self.enemies<self.board.enemies:
            enemy=EnemyGraphicsItem(self.board.enemies[-1])
            self.enemies.append(self.board.enemies[-1])
            self.scene.addItem(enemy)
        if self.board.enemyFinished==True:
            self.board.enemyFinished=False
            for i in self.enemies:
                if i.is_finished==True:
                    del i
        if self.board.enemyDead==True:
            self.board.enemyDead=False
            for i in self.enemies:
                if i.is_dead==True:
                    del i
        for enemy_item in self.get_enemy_graphics_items():
            if enemy_item.enemy.is_finished==True or enemy_item.enemy.is_dead==True:
                self.scene.removeItem(enemy_item)
            enemy_item.updateAll()

