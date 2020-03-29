from math import floor
from globals import enemyPath, squareSize
from coordinates import *
from board import *
from math import *

class Tower(object):

    def __init__(self):
        self.board=None
        self.position_x=-100
        self.position_y=-100
        self.is_purchasable=False
        self.is_selected=False
        self.level=1
        self.damage=3
        self.shotrange=100
        self.shot_delay = 3
        self.ticks_until_shoot=3
        self.targets=[]
        self.current_target=None

    def set_board(self,board, location):
        self.board=board
        self.position_x=location.get_x()*squareSize+squareSize/2
        self.position_y=location.get_y()*squareSize+squareSize/2

    def get_range(self):
        return self.shotrange

    def in_range(self,enemy):
        return self.shotrange>=sqrt(pow(self.position_x-enemy.position_x,2)+pow(self.position_y-enemy.position_y,2))

    def update_targets(self,enemies):
        self.targets=[]
        for i in enemies:
            if self.in_range(i) and i.is_dead==False:
                self.targets.append(i)
            else:
                if i in self.targets:
                    self.targets.remove(i)

    def update_current_target(self):
        if self.targets==[]:
            self.current_target=None
        else:
            first=self.targets[0]
            for i in self.targets:
                if i.distance>first.distance:
                    first=i
            self.current_target=first
