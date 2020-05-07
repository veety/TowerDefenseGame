from board import *
from math import *

class Tower(object):

    def __init__(self):
        self.board=None
        self.square_size=40
        self.graphicsItem=None
        self.position_x=-100
        self.position_y=-100
        self.is_purchasable=False
        self.is_selected=False

        self.targets=[]
        self.current_target=None

    def set_board(self,board, location):
        self.board=board
        self.position_x=location[0]*self.square_size+self.square_size/2
        self.position_y=location[1]*self.square_size+self.square_size/2

    def get_coordinates(self):
        return [self.position_x/self.square_size-1/2,self.position_y/self.square_size-1/2]

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

class Tower1(Tower):
    def __init__(self):
        super().__init__()
        self.type=1
        self.cost = 50
        self.sellValue = 20

        self.damage=4
        self.maxDamage=6
        self.shotrange=125
        self.maxRange=500
        self.shot_delay = 6
        self.minDelay=1

        self.ticks_until_shoot=self.shot_delay
        self.upgrades=['range',60,'delay',100]

class Tower2(Tower):
    def __init__(self):
        super().__init__()
        self.type=2
        self.cost = 100
        self.sellValue = 30

        self.damage = 4
        self.maxDamage = 16
        self.shotrange = 175
        self.maxRange = 300
        self.shot_delay = 5
        self.minDelay = 1

        self.ticks_until_shoot = self.shot_delay
        self.upgrades=['dmg',90,'range',40]

class FreezeTower(Tower):
    def __init__(self):
        super().__init__()
        self.type = 3
        self.cost = 200
        self.sellValue = 50

        self.damage = 0
        self.maxDamage = 0
        self.shotrange = 125
        self.maxRange = 250
        self.shot_delay = 10
        self.minDelay = 5
        self.freezeTime = 120

        self.ticks_until_shoot = self.shot_delay
        self.upgrades=['delay',200,'range',50]

class Tower4(Tower):
    def __init__(self):
        super().__init__()
        self.type = 4
        self.cost = 500
        self.sellValue = 100
        self.damage = 2
        self.maxDamage = 10
        self.shotrange = 175
        self.maxRange = 300
        self.shot_delay = 1
        self.minDelay = 5

        self.ticks_until_shoot = self.shot_delay
        self.upgrades = ['dmg', 110, 'range', 40]