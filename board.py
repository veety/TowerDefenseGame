import sys, time
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from square import Square
from tower import *
from enemy import *
from gui import *
from projectile import *

class gameBoard():

    def __init__(self):
        self.boardWidth=20
        self.boardHeight=20
        self.square_size=40
        self.read_config()
        self.board_setup()
        self.enemyFinished=False
        self.enemyDead=False
        self.enemies=[]
        self.towers=[]
        self.currentWave=0                              #int for wave number
        self.current_wave=self.waves[self.currentWave]  #list of content in current wave
        self.upcomingEnemies=0
        self.waveFinished=False
        self.wavesPassed=0
        for i in self.current_wave:
            if not i.isdigit():
                self.upcomingEnemies += 1

    def read_config(self):
        config=open("config.txt","r")
        self.money=int(config.readline().split(":")[1].lstrip().strip())
        self.health=int(config.readline().split(":")[1].lstrip().strip())
        path=config.readline().split(":")[1].lstrip().strip()
        self.enemyPath=[[0,2]]
        for i in path:
            if i == 'U': self.enemyPath.append([self.enemyPath[-1][0],self.enemyPath[-1][1] - 1])
            elif i == 'D': self.enemyPath.append([self.enemyPath[-1][0],self.enemyPath[-1][1] + 1])
            elif i == 'R': self.enemyPath.append([self.enemyPath[-1][0] + 1, self.enemyPath[-1][1]])
            elif i == 'L': self.enemyPath.append([self.enemyPath[-1][0] - 1, self.enemyPath[-1][1]])
        self.waves=config.readlines()
        self.waves = [line.rstrip('\n').rstrip(',').lstrip('\t').lstrip('[').rstrip(']').split(',') for line in self.waves]
        self.waves.pop(0)
        self.waves.pop(-1)

    def next_wave(self, event):
        if self.waveFinished==True:
            self.waveFinished=False
            self.currentWave+=1
            self.wavesPassed+=1
            try:
                self.current_wave = self.waves[self.currentWave]
                self.upcomingEnemies =0
                for i in self.current_wave:
                    if not i.isdigit():
                        self.upcomingEnemies += 1
            except:
                pass
        else:
            pass

    def move_enemies(self):
        for i in self.enemies:
            i.move()

    def board_setup(self):
        self.squares = [None] * self.boardWidth
        for x in range(self.get_width()):
            self.squares[x]=[None]*self.boardHeight
            for y in range(self.get_height()):
                if [x,y] in self.enemyPath:
                    self.squares[x][y]=Square(True,self,x,y)
                else:
                    self.squares[x][y] = Square(False,self,x,y)

    def get_width(self):
        return len(self.squares)

    def get_height(self):
        return len(self.squares[0])

    def get_square(self,location):
        return self.squares[location[0]][location[1]]

    def add_enemy(self,enemy,location,direction):
        enemy.set_board(self,location,direction)
        self.enemies.append(enemy)
        self.get_square(location).set_enemy(enemy)

    def remove_enemy(self,enemy):
        self.enemies.remove(enemy)

    def remove_tower(self,tower):
        self.towers.remove(tower)
        self.gui.towers.remove(tower)
        self.gui.scene.removeItem(tower.graphicsItem)

    def add_tower(self,tower,location):
        tower.set_board(tower,location)
        self.money-=tower.cost
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

    def add_projectile(self,tower,target):
        x=tower.position_x
        y=tower.position_y
        projectile=Projectile(target,x,y)
        target.projectilecount+=1
        self.gui.scene.addItem(projectile)

    def shoot(self,tower,enemy):
        try:
            enemy.health-=tower.damage
            self.add_projectile(tower, enemy)
            if type(tower) == FreezeTower:
                enemy.frozen = tower.freezeTime
        except:
            pass

    def wave_finished(self):
        if self.waves[self.currentWave]==[]:                   #Kun ei ole tulossa lisää, palautetaan True.
            self.waveFinished=True
            for i in self.enemies:
                if i.is_finished == False and i.is_dead == False:   #Jos kuitenkin vihollisia on vielä tuhoamatta,
                    self.waveFinished=False                         #self.waveFinished pidetään epätotena kunnes kaikki on tuhottu.
            return True
        else:
            return False

    def lose(self):
        self.gui.lose_screen()

    def win(self):
        self.gui.win_screen()

    def wave_manager(self):
        if self.health<=0:
            self.lose()
        if len(self.waves)==self.currentWave+1 and self.waveFinished:
            self.win()
        if not self.wave_finished():
            if self.current_wave[0]=='a':
                self.current_wave.pop(0)
                a = EnemyA(self.enemyPath[0][0] * self.square_size + self.square_size/2, self.enemyPath[0][1] * self.square_size + self.square_size/2)
                a.location = self.enemyPath[0]
                a.direction = 'RIGHT'
                self.add_enemy(a, a.location, a.direction)
                self.upcomingEnemies-=1
            elif self.current_wave[0]=='b':
                self.current_wave.pop(0)
                b = EnemyB(self.enemyPath[0][0] * self.square_size + self.square_size / 2, self.enemyPath[0][1] * self.square_size + self.square_size / 2)
                b.location = self.enemyPath[0]
                b.direction = 'RIGHT'
                self.add_enemy(b, b.location, b.direction)
                self.upcomingEnemies -= 1
            elif self.current_wave[0]=='c':
                self.current_wave.pop(0)
                c = EnemyC(self.enemyPath[0][0] * self.square_size + self.square_size / 2, self.enemyPath[0][1] * self.square_size + self.square_size / 2)
                c.location = self.enemyPath[0]
                c.direction = 'RIGHT'
                self.add_enemy(c, c.location, c.direction)
                self.upcomingEnemies -= 1
            else:
                self.current_wave[0]=int(self.current_wave[0])-1
                if self.current_wave[0] == 0:
                    self.current_wave.pop(0)

