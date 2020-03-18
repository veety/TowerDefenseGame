import sys, time, json
from PyQt5 import QtCore, QtGui
import globals
from square import Square
from globals import *

class gameBoard():

    def __init__(self,boardWidth,boardHeight):
        self.squares=[None]*boardWidth
        for x in range(self.get_width()):
            self.squares[x]=[None]*boardHeight
            for y in range(self.get_height()):
                if [x,y] in globals.enemyPath:
                    self.squares[x][y]=Square(True)
                else:
                    self.squares[x][y] = Square(False)
        self.robots=[]
        self.towers=[]

    def get_width(self):
        return len(self.squares)

    def get_height(self):
        return len(self.squares[0])

    def get_square(self,coordinates):
        if self.contains(coordinates):
            return self.squares[coordinates.get_x()][coordinates.get_y()]
        else:
            return Square(True)

    def contains(self, coordinates):
        x_coordinate = coordinates.get_x()
        y_coordinate = coordinates.get_y()
        return 0 <= x_coordinate < self.get_width() and 0 <= y_coordinate < self.get_height()