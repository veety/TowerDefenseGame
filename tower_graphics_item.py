from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QLabel, QGraphicsProxyWidget
from math import *
from enemy import *

class TowerGraphicsItem(QtWidgets.QGraphicsPixmapItem):

    def __init__(self,tower,gui):
        super(TowerGraphicsItem, self).__init__()
        self.gui=gui
        self.tower=tower
        self.tower.graphicsItem=self
        self.square_size=40
        self.selected=False
        self.pixmap=QPixmap()
        if self.tower.type==1:
            self.pixmap.load("items/tower_1.png")
        elif self.tower.type == 2:
            self.pixmap.load("items/tower_2.png")
        elif self.tower.type == 3:
            self.pixmap.load("items/tower_freeze.png")
        elif self.tower.type == 4:
            self.pixmap.load("items/tower_4.png")
        self.setPixmap(self.pixmap)
        self.drawRange=False
        self.setX(self.tower.position_x - self.square_size / 2)
        self.setY(self.tower.position_y - self.square_size / 2)
        self.setTransformOriginPoint(self.square_size / 2, self.square_size / 2)
        self.updateRotation()

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

    def mousePressEvent(self, event):
        if self.tower.is_purchasable==False and self.gui.towerMenu==False and self.gui.tower_selected==None:
            self.gui.towerMenu=True
            self.gui.draw_range(self.tower, self.tower.position_x/self.square_size-1/2, self.tower.position_y/self.square_size-1/2, True)
            self.gui.tower_menu_(self.tower, self.tower.position_x+1.5*self.square_size+101,self.tower.position_y+118)

class ShopTowerGraphicsItem(TowerGraphicsItem):

    def __init__(self,tower,gui):
        super(ShopTowerGraphicsItem,self).__init__(tower,gui)
        self.pixmap=self.pixmap.scaled(100, 100)
        self.setPixmap(self.pixmap)

    def mousePressEvent(self, event):
        if self.tower.is_purchasable==True and self.gui.tower_selected==None and self.gui.towerMenu==False:
            self.gui.tower_selected=self.tower
