from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from board import *
from enemy_graphics_item import *
from tower_graphics_item import *
from boardgriditem import *
from projectile import *
from range import *
import os, sys

class GUI(QtWidgets.QMainWindow):
    def __init__(self,board):
        super().__init__()
        self.board = board
        self.board.gui = self
        self.enemies = []
        self.towers = []
        self.projectiles = []
        self.tower_selected = None
        self.selectedTower = None
        self.towerMenu = False

        self.setCentralWidget(QtWidgets.QWidget())
        self.horizontal=QtWidgets.QHBoxLayout()
        self.centralWidget().setLayout(self.horizontal)
        self.setMouseTracking(True)
        self.init_window()
        self.add_board_grid_items()
        self.add_shop_tower_items()

    def init_window(self):                                  #Sets up background, labels, buttons, QGraphicsScene and QGraphicsView.
        oImage=QImage("gui/background.png")
        palette=QPalette()
        palette.setBrush(QPalette.Window,QBrush(oImage))
        self.setPalette(palette)
        self.setGeometry(0,0,1920,1080)
        self.setWindowTitle('Tower Defense')
        self.setFixedSize(1920,1080)

        self.speed=QtWidgets.QLabel(self)
        self.speed1=QPixmap()
        self.speed1.load("gui/speed1.png")
        self.speed2 = QPixmap()
        self.speed2.load("gui/speed2.png")
        self.speed3 = QPixmap()
        self.speed3.load("gui/speed3.png")
        self.speed.setPixmap(self.speed1)
        self.speed.setFixedSize(124,124)
        self.speed.move(1172,136)
        self.speed.mousePressEvent=self.speed_switch

        self.waveFinished = QtWidgets.QLabel(self)
        self.waveFinished.setFont(QtGui.QFont("Times",25,QtGui.QFont.Bold))
        self.waveFinished.setFixedSize(300, 65)
        self.waveFinished.move(598, 63)
        self.waveFinished.mousePressEvent = self.board.next_wave

        self.health = QtWidgets.QLabel(self)
        self.health.setFont(QtGui.QFont("Times",25,QtGui.QFont.Bold))
        self.health.setFixedSize(370,55)
        self.health.move(1320,144)

        self.money = QtWidgets.QLabel(self)
        self.money.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.money.setFixedSize(370,55)
        self.money.move(1320, 199)

        self.upcomingEnemies = QtWidgets.QLabel(self)
        self.upcomingEnemies.setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))
        self.upcomingEnemies.setFixedSize(300, 65)
        self.upcomingEnemies.move(116, 63)

        self.wave = QtWidgets.QLabel(self)
        self.wave.setFont(QtGui.QFont("Times", 30, QtGui.QFont.Bold))
        self.wave.setFixedSize(70,70)
        self.wave.move(489, 60)

        self.show()

        self.scene=QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0,0,1719,804)

        self.view=QGraphicsView(self.scene,self)
        self.view.setMouseTracking(True)
        self.view.adjustSize()
        self.view.setStyleSheet("background:transparent;")
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.show()
        self.horizontal.addWidget(self.view)

    '''
    Down from here: Methods for updating items and labels in scene. Called from timer with interval of some milliseconds.
    '''

    def update_all(self):
        self.update_towers()
        self.update_projectiles()
        self.update_enemies()
        self.update_labels()

    def update_towers(self):
        if self.towers < self.board.towers:
            tower=TowerGraphicsItem(self.board.towers[-1],self)
            self.towers.append(self.board.towers[-1])
            self.scene.addItem(tower)
        for tower_item in self.get_tower_graphics_items():
            tower_item.updateRotation()

    def update_projectiles(self):
        for projectile in self.get_projectiles():
            if projectile.finished == True:
                projectile.target.projectilecount-=1
                self.scene.removeItem(projectile)
                if projectile.target.is_dead and projectile.target.projectilecount==0:
                    self.scene.removeItem(projectile.target.graphicsItem)
            projectile.updateAll()

    def update_enemies(self):
        if self.enemies<self.board.enemies:
            if type(self.board.enemies[-1])==EnemyA:
                enemy=EnemyGraphicsItemA(self, self.board.enemies[-1])
            elif type(self.board.enemies[-1])==EnemyB:
                enemy=EnemyGraphicsItemB(self, self.board.enemies[-1])
            elif type(self.board.enemies[-1])==EnemyC:
                enemy=EnemyGraphicsItemC(self, self.board.enemies[-1])
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
            if enemy_item.enemy.is_finished==True:
                self.scene.removeItem(enemy_item)
            enemy_item.updateAll()

    def update_labels(self):
        healthText="Health: "+str(self.board.health)
        moneyText = "Money: " + str(self.board.money)
        enemiesComingText = "Enemies coming: " + str(self.board.upcomingEnemies)
        waveNumberText = str(self.board.wavesPassed+1)
        if self.board.waveFinished==True:
            waveText="    Next Wave"
        else:
            waveText=""
        self.health.setText(healthText)
        self.money.setText(moneyText)
        self.upcomingEnemies.setText(enemiesComingText)
        self.waveFinished.setText(waveText)
        self.wave.setText(waveNumberText)
        try:
            statsText=" Range: " +str(self.selectedTower.shotrange) +"  Delay: " +str(self.selectedTower.shot_delay) +"  Damage: " +str(self.selectedTower.damage)
            self.stats.setText(statsText)
        except:
            pass

    '''
    Down from here:     Methods that create labels and methods that are called by clicking these labels.
                        Basically every label that is not created in init.
    '''

    def tower_menu_(self,tower,x,y):
        self.selectedTower=tower
        self.tower_menu=QtWidgets.QLabel(self)
        self.tower_Menu=QPixmap()
        self.tower_Menu.load("gui/towerMenu.png")
        self.tower_menu.setPixmap(self.tower_Menu)
        self.tower_menu.setFixedSize(400,300)
        self.tower_menu.move(x,y)
        self.tower_menu.show()

        self.closeMenu=QtWidgets.QLabel(self)
        self.close_Menu=QPixmap()
        self.close_Menu.load("gui/closeMenu.png")
        self.closeMenu.setPixmap(self.close_Menu)
        self.closeMenu.setFixedSize(92,92)
        self.closeMenu.move(x+304,y+4)
        self.closeMenu.mousePressEvent=self.close_menu
        self.closeMenu.show()

        self.sell_tower = QtWidgets.QLabel(self)
        text="      + "+str(self.selectedTower.sellValue)
        self.sell_tower.setText(text)
        self.sell_tower.setFont(QtGui.QFont("Times",14,QtGui.QFont.Bold))
        self.sell_tower.setFixedSize(127, 39)
        self.sell_tower.move(x + 251, y + 182)
        self.sell_tower.mousePressEvent = self.sell_tower_
        self.sell_tower.show()

        self.toUpgrade=self.selectedTower.upgrades          #Format [Upgrade 1 type, Upgrade 1 cost, Upgrade 2 type, Upgrade 2 cost]

        self.upgrade1type=QtWidgets.QLabel(self)
        text = " " + self.toUpgrade[0]
        self.upgrade1type.setText(text)
        self.upgrade1type.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))
        self.upgrade1type.setFixedSize(76, 39)
        self.upgrade1type.move(x + 23, y + 139)
        self.upgrade1type.show()

        self.upgrade1=QtWidgets.QLabel(self)
        text="      - "+str(self.toUpgrade[1])
        self.upgrade1.setText(text)
        self.upgrade1.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))
        self.upgrade1.setFixedSize(127, 39)
        self.upgrade1.move(x + 104, y + 139)
        self.upgrade1.mousePressEvent = self.upgrade_1
        self.upgrade1.show()

        self.upgrade2type = QtWidgets.QLabel(self)
        text=" "+self.toUpgrade[2]
        self.upgrade2type.setText(text)
        self.upgrade2type.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))
        self.upgrade2type.setFixedSize(76, 39)
        self.upgrade2type.move(x + 23, y + 182)
        self.upgrade2type.show()

        self.upgrade2 = QtWidgets.QLabel(self)
        text = "      - " + str(self.toUpgrade[3])
        self.upgrade2.setText(text)
        self.upgrade2.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))
        self.upgrade2.setFixedSize(127, 39)
        self.upgrade2.move(x + 104, y + 182)
        self.upgrade2.mousePressEvent = self.upgrade_2
        self.upgrade2.show()

        self.stats = QtWidgets.QLabel(self)
        self.stats.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.stats.setFixedSize(400, 39)
        self.stats.move(x+4, y+4)
        self.stats.show()

    def upgrade_1(self,event):                              #Purchases upgrade 1
        if self.board.money>=self.toUpgrade[1]:
            if self.toUpgrade[0]=='range' and self.selectedTower.shotrange<self.selectedTower.maxRange:
                self.selectedTower.shotrange+=50
                self.board.money -= self.toUpgrade[1]
                self.draw_range(1,2,3,False)
                self.draw_range(self.selectedTower, self.selectedTower.get_coordinates()[0], self.selectedTower.get_coordinates()[1], True)
            elif self.toUpgrade[0]=='dmg' and self.selectedTower.damage<self.selectedTower.maxDamage:
                self.selectedTower.damage+=1
                self.board.money -= self.toUpgrade[1]
            elif self.toUpgrade[0]=='delay' and self.selectedTower.shot_delay>self.selectedTower.minDelay:
                self.selectedTower.shot_delay-=1
                self.board.money -= self.toUpgrade[1]

    def upgrade_2(self,event):                              #Purchases upgrade 2
        if self.board.money >= self.toUpgrade[3]:
            if self.toUpgrade[2]=='range' and self.selectedTower.shotrange<self.selectedTower.maxRange:
                self.selectedTower.shotrange+=50
                self.board.money -= self.toUpgrade[3]
                self.draw_range(1, 2, 3, False)
                self.draw_range(self.selectedTower, self.selectedTower.get_coordinates()[0], self.selectedTower.get_coordinates()[1], True)
            elif self.toUpgrade[2]=='dmg' and self.selectedTower.damage<self.selectedTower.maxDamage:
                self.selectedTower.damage+=1
                self.board.money -= self.toUpgrade[3]
            elif self.toUpgrade[2]=='delay' and self.selectedTower.shot_delay>self.selectedTower.minDelay:
                self.selectedTower.shot_delay -= 1
                self.board.money -= self.toUpgrade[3]

    def sell_tower_(self,event):                            #Sells tower whose upgrade menu is open. Closes upgrade menu.
        self.board.money+=self.selectedTower.sellValue
        self.tower_menu.deleteLater()
        self.closeMenu.deleteLater()
        self.sell_tower.deleteLater()
        self.board.remove_tower(self.selectedTower)
        self.upgrade1.deleteLater()
        self.upgrade1type.deleteLater()
        self.upgrade2.deleteLater()
        self.upgrade2type.deleteLater()
        self.stats.deleteLater()
        self.board.squares[int(self.selectedTower.get_coordinates()[0])][int(self.selectedTower.get_coordinates()[1])].tower = None
        self.selectedTower=None
        self.draw_range(1,2,3,False)
        self.towerMenu=False

    def close_menu(self,event):                             #Closes upgrade menu.
        self.tower_menu.deleteLater()
        self.closeMenu.deleteLater()
        self.sell_tower.deleteLater()
        self.upgrade1.deleteLater()
        self.upgrade1type.deleteLater()
        self.upgrade2.deleteLater()
        self.upgrade2type.deleteLater()
        self.stats.deleteLater()
        self.selectedTower=None
        self.draw_range(1,2,3,False)
        self.towerMenu=False

    def win_screen(self):

        self.win=QtWidgets.QLabel(self)
        self.winLabel=QPixmap()
        self.winLabel.load("gui/winScreen.png")
        self.win.setPixmap(self.winLabel)
        self.win.setFixedSize(1078,761)
        self.win.move(422,145)
        self.win.show()

        self.exit = QtWidgets.QLabel(self)
        self.exitButton = QPixmap()
        self.exitButton.load("gui/exitButton.png")
        self.exit.setPixmap(self.exitButton)
        self.exit.setFixedSize(244, 104)
        self.exit.move(597, 713)
        self.exit.mousePressEvent = self.exit_
        self.exit.show()

        self.restart=QtWidgets.QLabel(self)
        self.restartButton=QPixmap()
        self.restartButton.load("gui/restartButton.png")
        self.restart.setPixmap(self.restartButton)
        self.restart.setFixedSize(244, 104)
        self.restart.move(1081, 713)
        self.restart.mousePressEvent = self.restart_
        self.restart.show()

    def lose_screen(self):

        self.lose=QtWidgets.QLabel(self)
        self.loseLabel=QPixmap()
        self.loseLabel.load("gui/loseScreen.png")
        self.lose.setPixmap(self.loseLabel)
        self.lose.setFixedSize(1078,761)
        self.lose.move(422,145)
        self.lose.show()

        self.exit = QtWidgets.QLabel(self)
        self.exitButton = QPixmap()
        self.exitButton.load("gui/exitButton.png")
        self.exit.setPixmap(self.exitButton)
        self.exit.setFixedSize(244, 104)
        self.exit.move(597, 713)
        self.exit.mousePressEvent = self.exit_
        self.exit.show()

        self.restart=QtWidgets.QLabel(self)
        self.restartButton=QPixmap()
        self.restartButton.load("gui/restartButton.png")
        self.restart.setPixmap(self.restartButton)
        self.restart.setFixedSize(244, 104)
        self.restart.move(1081, 713)
        self.restart.mousePressEvent = self.restart_
        self.restart.show()

    def exit_(self,event):                                  #Exits the game, no replacing process.
        os.execv(NotHinG, sys.argv)

    def restart_(self,event):                               #Exits the game, starts new game as replacing process.
        path = os.path.realpath(__file__)                   #ONLY WORKS WHEN USING EXE, NOT PY!!!
        path = path.strip("gui.pyc")
        path = path + "launcher.exe"
        os.execv(path, sys.argv)

    def speed_switch(self,event):                           #Changes timer's intervals.
        speed=self.timer.speed_()
        if speed==1:
            self.speed.setPixmap(self.speed1)
        if speed==2:
            self.speed.setPixmap(self.speed2)
        if speed==3:
            self.speed.setPixmap(self.speed3)

    '''
    Down from here:     Methods for getting lists of different items.
    '''

    def get_enemy_graphics_items(self):
        items=[]
        for item in self.scene.items():
            if isinstance(item, EnemyGraphicsItem):
                items.append(item)
        return items

    def get_board_grid_items(self):
        items=[]
        for item in self.scene.items():
            if type(item) is BoardGridItem:
                items.append(item)
        return items

    def get_tower_graphics_items(self):
        items=[]
        for item in self.scene.items():
            if isinstance(item, TowerGraphicsItem):
                items.append(item)
        return items

    def get_projectiles(self):
        items = []
        for item in self.scene.items():
            if type(item) is Projectile:
                items.append(item)
        return items

    '''
    Down from here:     Misc.
    '''

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_P:
            self.timer.pause()
        if event.key() == QtCore.Qt.Key_Space:
            if self.board.waveFinished == True:
                self.board.next_wave(-1)
            else:
                self.speed_switch(event)

    def add_shop_tower_items(self):
        self.tower1=Tower1()
        self.tower1.is_purchasable=True
        self.tower1.position_x = 1212
        self.tower1.position_y = 185
        self.tower1item=ShopTowerGraphicsItem(self.tower1,self)
        self.scene.addItem(self.tower1item)

        self.tower2=Tower2()
        self.tower2.is_purchasable = True
        self.tower2.position_x = 1476
        self.tower2.position_y = 185
        self.tower2item = ShopTowerGraphicsItem(self.tower2, self)
        self.scene.addItem(self.tower2item)

        self.tower3 = FreezeTower()
        self.tower3.is_purchasable = True
        self.tower3.position_x = 1212
        self.tower3.position_y = 410
        self.tower3item = ShopTowerGraphicsItem(self.tower3, self)
        self.scene.addItem(self.tower3item)

        self.tower4 = Tower4()
        self.tower4.is_purchasable = True
        self.tower4.position_x = 1476
        self.tower4.position_y = 410
        self.tower4item = ShopTowerGraphicsItem(self.tower4, self)
        self.scene.addItem(self.tower4item)

    def add_board_grid_items(self):
        for i in range(self.board.get_width()):
            for j in range(self.board.get_height()):
                ispath=self.board.get_square([i,j]).is_path()
                if ispath:
                    rectangle=BoardgridItem(i,j,True,self)
                else:
                    rectangle=BoardgridItem(i,j,False,self)
                self.scene.addItem(rectangle)

    def draw_range(self, tower, x, y, OnOff):
        if OnOff==True:
            self.range=Range(x,y,tower.shotrange)
            self.scene.addItem(self.range)
        else:
            self.scene.removeItem(self.range)
