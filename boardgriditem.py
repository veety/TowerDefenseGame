from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import *
from tower import *
from PyQt5.QtWidgets import QGraphicsPixmapItem

class BoardgridItem(QGraphicsPixmapItem):
    def __init__(self,x,y,ispath,gui):
        super(QGraphicsPixmapItem, self).__init__()
        self.setAcceptHoverEvents(True)
        self.gui = gui
        self.x = x
        self.y = y
        self.square_size = 40
        self.ispath = ispath
        self.pixmap = QPixmap()
        self.setTransformOriginPoint(self.x, self.y)
        self.showRange=False
        if [self.x,self.y]==self.gui.board.enemyPath[0] or [self.x,self.y]==self.gui.board.enemyPath[-1]:
            self.pixmap.load("items/LR.png")
            self.setPixmap(self.pixmap)
        elif self.ispath:
            neighboring=self.gui.board.get_square([self.x,self.y]).get_neighboring()
            if [self.x - 1,self.y] in neighboring and [self.x,self.y - 1] in neighboring and [self.x + 1,self.y] in neighboring and [self.x, self.y + 1] in neighboring:
                self.pixmap.load("items/URDL.png")
            elif [self.x - 1,self.y] in neighboring and [self.x,self.y - 1] in neighboring and [self.x + 1,self.y] in neighboring:
                self.pixmap.load("items/LUR.png")
            elif [self.x - 1, self.y] in neighboring and [self.x, self.y - 1] in neighboring and [self.x, self.y + 1] in neighboring:
                self.pixmap.load("items/DLU.png")
            elif [self.x + 1, self.y] in neighboring and [self.x - 1, self.y] in neighboring and [self.x, self.y + 1] in neighboring:
                self.pixmap.load("items/RDL.png")
            elif [self.x, self.y - 1] in neighboring and [self.x + 1, self.y] in neighboring and [self.x, self.y + 1] in neighboring:
                self.pixmap.load("items/URD.png")
            elif [self.x - 1,self.y] in neighboring and [self.x,self.y - 1] in neighboring:
                self.pixmap.load("items/UL.png")
            elif [self.x - 1,self.y] in neighboring and [self.x,self.y + 1] in neighboring:
                self.pixmap.load("items/DL.png")
            elif [self.x,self.y - 1] in neighboring and [self.x + 1,self.y] in neighboring:
                self.pixmap.load("items/UR.png")
            elif [self.x,self.y + 1] in neighboring and [self.x + 1,self.y] in neighboring:
                self.pixmap.load("items/DR.png")
            elif [self.x,self.y + 1] in neighboring and [self.x,self.y - 1] in neighboring:
                self.pixmap.load("items/UD.png")
            elif [self.x + 1,self.y] in neighboring and [self.x - 1,self.y] in neighboring:
                self.pixmap.load("items/LR.png")
            elif [self.x + 1, self.y] in neighboring:
                self.pixmap.load("items/R.png")
            elif [self.x, self.y + 1] in neighboring:
                self.pixmap.load("items/D.png")
            elif [self.x - 1, self.y] in neighboring:
                self.pixmap.load("items/L.png")
            elif [self.x, self.y - 1] in neighboring:
                self.pixmap.load("items/U.png")
            else:
                self.pixmap.load("items/path.png")
            self.setPixmap(self.pixmap)
        else:
            self.pixmap.load("items/grass.png")
            self.setPixmap(self.pixmap)
        self.setX(self.square_size * self.x)
        self.setY(self.square_size * self.y)

    def mousePressEvent(self, event):
        if self.gui.tower_selected!=None and not self.ispath:
            if self.gui.board.money>=self.gui.tower_selected.cost and self.gui.board.squares[self.x][self.y].get_tower()==None:
                tower=Tower()
                self.gui.board.add_tower(tower,[self.x,self.y])
        self.gui.tower_selected=None

    def hoverEnterEvent(self, event):
        if self.gui.tower_selected!=None:
            if self.ispath==False:
                self.pixmap.load("items/grassRed.png")
                self.setPixmap(self.pixmap)
                self.gui.draw_range(self.gui.tower_selected,self.x,self.y,True)
                self.showRange=True

    def hoverLeaveEvent(self, event):                                           #Deletes range circle
        if self.ispath==False and self.showRange==True:
            self.pixmap.load("items/grass.png")
            self.setPixmap(self.pixmap)
            if self.gui.towerMenu==False:
                self.gui.draw_range(1,2,3,False)
            self.showRange=False

    def mousePressEvent(self, event):
        if self.gui.tower_selected!=None and not self.ispath:
            if self.gui.board.money>=self.gui.tower_selected.cost and self.gui.board.squares[self.x][self.y].get_tower()==None:
                if self.gui.tower_selected.type==1:
                    tower=Tower1()
                if self.gui.tower_selected.type==2:
                    tower=Tower2()
                if self.gui.tower_selected.type==3:
                    tower=FreezeTower()
                if self.gui.tower_selected.type==4:
                    tower=Tower4()
                self.gui.board.add_tower(tower,[self.x,self.y])
                self.gui.draw_range(1,2,3,False)
                self.pixmap.load("items/grass.png")
                self.setPixmap(self.pixmap)
        self.gui.tower_selected=None