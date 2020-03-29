from math import floor
from globals import enemyPath, squareSize
from coordinates import *
from board import *

class Enemy(object):

    def __init__(self,x,y):
        self.path=[]
        for i in enemyPath:
            self.path.append(i)
        self.board=None
        self.current_block=enemyPath[0]
        self.position_x=x
        self.position_y=y
        self.is_finished=False
        self.is_dead=False
        self.speed=1
        self.health=10
        self.distance=0
        self.direction=None

    def get_board(self):
        return self.board

    def set_brain(self, new_brain):
        self.brain=new_brain

    def get_brain(self):
        return self.brain

    def get_direction(self):
        return self.direction

    def get_current_block(self):
        return Coordinates(int(floor(self.position_x/squareSize)), int(floor(self.position_y/squareSize)))

    def get_location_square(self):
        return self.get_board().get_square(self.get_current_block())

    def destroy(self):
        self.is_dead=True

    def finished(self):
        self.is_finished=True

    def set_board(self,board, location, direction):
        self.board=board
        self.position_x=location.get_x()*squareSize+squareSize/2
        self.position_y=location.get_y()*squareSize+squareSize/2
        self.direction=direction

    def get_next_block(self):
        if self.direction=="RIGHT":
            return [self.get_current_block().get_x()+1, self.get_current_block().get_y()]
        elif self.direction=="LEFT":
            return [self.get_current_block().get_x()-1, self.get_current_block().get_y()]
        elif self.direction=="UP":
            return [self.get_current_block().get_x(), self.get_current_block().get_y()-1]
        elif self.direction=="DOWN":
            return [self.get_current_block().get_x(), self.get_current_block().get_y()+1]
        return None

    def move(self):
        temp=[self.get_current_block().get_x(),self.get_current_block().get_y()]
        if self.get_next_block()!=temp:
            try:
                if self.path[1]!=self.get_next_block() and self.position_x%squareSize==squareSize/2 and self.position_y%squareSize==squareSize/2:
                    self.path.pop(0)
                    if self.get_current_block().get_y()<self.path[1][1]:
                        self.direction="DOWN"
                    if self.get_current_block().get_y()>self.path[1][1]:
                        self.direction = "UP"
                    if self.get_current_block().get_x() < self.path[1][0]:
                        self.direction = "RIGHT"
                    if self.get_current_block().get_x() > self.path[1][0]:
                        self.direction = "LEFT"
            except:
                self.is_finished=True
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
            self.board.enemyDead=True

  #  class RedCircle(Enemy):
  #      def __init__(self):
   #         super(RedCircle, self).__init__()
   #         self.health = 200
   #         self.speed = 2
   #         self.color = QtGui.QColor(25, 180, 10, 255)

 #   class GreenCircle(Enemy):
  #      def __init__(self):
  #          super(GreenCircle, self).__init__()
  #          self.health = 100
  #          self.speed = 2
 #           self.color = QtGui.QColor(25, 180, 10, 255)

 #   class BlueCircle(Enemy):
  #      def __init__(self):
  #          super(BlueCircle, self).__init__()
  #          self.health = 300
  #          self.speed = 2
   #         self.color = QtGui.QColor(25, 80, 100, 255)