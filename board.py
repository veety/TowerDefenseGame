import sys, time, json
import globals
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from square import Square
from globals import *
from coordinates import *
from enemy import Enemy
from gui import *

class gameBoard():

    def __init__(self):
        self.squares=[None]*boardWidth
        self.gui=None
        self.board_setup()
        self.enemyFinished=False
        self.enemyDead=False
        self.enemies=[]
        self.towers=[]
        self.current_wave=wave[0]

    def move_enemies(self):
        for i in self.enemies:
            i.move()

    def board_setup(self):
        for x in range(self.get_width()):
            self.squares[x]=[None]*boardHeight
            for y in range(self.get_height()):
                if [x,y] in globals.enemyPath:
                    self.squares[x][y]=Square(True,self,x,y)
                else:
                    self.squares[x][y] = Square(False,self,x,y)

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

    def add_enemy(self,enemy,location,direction):
        enemy.set_board(self,location,direction)
        self.enemies.append(enemy)
        self.get_square(location).set_enemy(enemy)

    def remove_enemy(self,enemy):
        self.enemies.remove(enemy)

    def add_tower(self,tower,location):
        tower.set_board(tower,location)
        self.towers.append(tower)
        self.get_square(location).set_tower(tower)

    def tower_updater(self):
        for i in self.towers:
            i.update_targets(self.enemies)
            i.update_current_target()
            if i.ticks_until_shoot==0:
                self.shoot(i,i.current_target)
                i.ticks_until_shoot=i.shot_delay
            else:
                i.ticks_until_shoot-=1

    def shoot(self,tower,enemy):
        try:
            enemy.health-=tower.damage
        except:
            pass

    def determine_direction(self, enemyPath):
        if enemyPath[0][0] < enemyPath[1][0]:
            return 'RIGHT'
        if enemyPath[0][0] > enemyPath[1][0]:
            return 'LEFT'
        if enemyPath[0][1] < enemyPath[1][1]:
            return 'UP'
        if enemyPath[0][1] > enemyPath[1][1]:
            return 'DOWN'

    def wave_manager(self):
        if self.current_wave==[]:
            pass
        else:
            if self.current_wave[0]=='a':
                self.current_wave.pop(0)
                a = Enemy(enemyPath[0][0] * squareSize + squareSize/2, enemyPath[0][1] * squareSize + squareSize/2)
                a.location = Coordinates(enemyPath[0][0],enemyPath[0][1])
                a.direction = self.determine_direction(enemyPath)
                self.add_enemy(a, a.location, a.direction)
            elif self.current_wave[0]=='b':
                self.current_wave.pop(0)
                b = Enemy(enemyPath[0][0] * squareSize + squareSize / 2, enemyPath[0][1] * squareSize + squareSize / 2)
                b.location = Coordinates(enemyPath[0][0],enemyPath[0][1])
                b.direction = self.determine_direction(enemyPath)
                self.add_enemy(b, b.location, b.direction)
            elif self.current_wave[0]=='c':
                self.current_wave.pop(0)
                c = Enemy(enemyPath[0][0] * squareSize + squareSize / 2, enemyPath[0][1] * squareSize + squareSize / 2)
                c.location = Coordinates(enemyPath[0][0],enemyPath[0][1])
                c.direction = self.determine_direction(enemyPath)
                self.add_enemy(c, c.location, c.direction)
            else:
                self.current_wave[0]=self.current_wave[0]-1
                if self.current_wave[0] == 0:
                    self.current_wave.pop(0)

