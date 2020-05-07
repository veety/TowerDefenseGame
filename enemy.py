from board import *

class Enemy(object):

    def __init__(self,x,y):
        self.square_size=40
        self.board=None
        self.graphicsItem=None
        self.projectilecount=0
        self.position_x=x
        self.position_y=y
        self.frozen=0
        self.is_finished=False
        self.is_dead=False
        self.distance=0
        self.direction=None
        self.didDamage=False
        self.droppedMoney=False
        self.immuneToFreeze=False

    def get_x(self):
        return self.position_x

    def get_y(self):
        return self.position_y

    def get_board(self):
        return self.board

    def get_direction(self):
        return self.direction

    def get_current_block(self):
        return [int(floor(self.position_x/self.square_size)), int(floor(self.position_y/self.square_size))]

    def get_location_square(self):
        return self.get_board().get_square(self.get_current_block())

    def finished(self):
        self.is_finished=True

    def set_board(self,board, location, direction):
        self.board=board
        self.position_x=location[0]*self.square_size+self.square_size/2
        self.position_y=location[1]*self.square_size+self.square_size/2
        self.direction=direction
        self.current_block=self.board.enemyPath[0]
        self.path=[]
        for i in self.board.enemyPath:
            self.path.append(i)

    def get_next_block(self):
        if self.direction=="RIGHT":
            return [self.get_current_block()[0]+1, self.get_current_block()[1]]
        elif self.direction=="LEFT":
            return [self.get_current_block()[0]-1, self.get_current_block()[1]]
        elif self.direction=="UP":
            return [self.get_current_block()[0], self.get_current_block()[1]-1]
        elif self.direction=="DOWN":
            return [self.get_current_block()[0], self.get_current_block()[1]+1]

    def move(self):
        if self.frozen>0 and self.immuneToFreeze==False:    #Freeze enemy for self.frozen ticks, no effect if has been frozen before
            self.frozen-=1
            if self.frozen==1:
                self.immuneToFreeze=True
            return 0
        temp=self.get_current_block()
        if self.get_next_block()!=temp:
            try:
                if self.path[1]!=self.get_next_block() and self.position_x%self.square_size==self.square_size/2 and self.position_y%self.square_size==self.square_size/2:
                    self.path.pop(0)
                    if self.get_current_block()[1]<self.path[1][1]:
                        self.direction="DOWN"
                    if self.get_current_block()[1]>self.path[1][1]:
                        self.direction = "UP"
                    if self.get_current_block()[0] < self.path[1][0]:
                        self.direction = "RIGHT"
                    if self.get_current_block()[0] > self.path[1][0]:
                        self.direction = "LEFT"
            except:
                self.is_finished=True
                if not self.didDamage and not self.is_dead:
                    self.board.health-=self.damage
                self.didDamage=True
        if self.is_finished==True:
            self.board.enemyFinished=True
        elif self.direction == "RIGHT":
            self.position_x += self.speed
        elif self.direction == "DOWN":
            self.position_y += self.speed
        elif self.direction == "LEFT":
            self.position_x -= self.speed
        elif self.direction == "UP":
            self.position_y -= self.speed
        self.distance+=self.speed
        if self.health<=0:
            self.is_dead=True
            if self.droppedMoney==False:
                self.droppedMoney=True
                self.board.money+=self.bounty
            self.board.enemyDead=True

class EnemyA(Enemy):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.speed = 1
        self.damage = 30
        self.bounty = 10
        self.health = 10

class EnemyB(Enemy):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.speed = 0.5
        self.damage = 30
        self.bounty = 15
        self.health = 60

class EnemyC(Enemy):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.speed = 1
        self.damage = 30
        self.bounty = 30
        self.health = 50