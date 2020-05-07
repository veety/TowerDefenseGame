from PyQt5 import QtCore
#from gui import GUI

class Timer():
    def __init__(self,gui,board):
        self.gui=gui
        self.board=board
        self.stopped=False
        self.gui.timer=self
        self.gameSpeed=0.5
        self.speed=1

        self.gui_timer=QtCore.QTimer()
        self.gui_timer.timeout.connect(self.gui.update_all)
        self.gui_timer.setInterval(15)
        self.gui_timer.start()

        self.enemy_timer=QtCore.QTimer()
        self.enemy_timer.timeout.connect(self.board.move_enemies)
        self.enemy_timer.setInterval(50/self.gameSpeed)
        self.enemy_timer.start()

        self.tower_timer=QtCore.QTimer()
        self.tower_timer.timeout.connect(self.board.tower_updater)
        self.tower_timer.setInterval(500/self.gameSpeed)
        self.tower_timer.start()

        self.wave_timer=QtCore.QTimer()
        self.wave_timer.timeout.connect(self.board.wave_manager)
        self.wave_timer.setInterval(2000/self.gameSpeed)
        self.wave_timer.start()

    def speed_(self):
        self.enemy_timer.stop()
        self.tower_timer.stop()
        self.wave_timer.stop()
        if self.speed==1:
            self.speed=2
            self.enemy_timer.setInterval(20/self.gameSpeed)
            self.tower_timer.setInterval(200/self.gameSpeed)
            self.wave_timer.setInterval(800/self.gameSpeed)
        elif self.speed==2:
            self.speed=3
            self.enemy_timer.setInterval(5/self.gameSpeed)
            self.tower_timer.setInterval(50/self.gameSpeed)
            self.wave_timer.setInterval(200/self.gameSpeed)
        elif self.speed==3:
            self.speed=1
            self.enemy_timer.setInterval(50/self.gameSpeed)
            self.tower_timer.setInterval(500/self.gameSpeed)
            self.wave_timer.setInterval(2000/self.gameSpeed)

        self.enemy_timer.start()
        self.tower_timer.start()
        self.wave_timer.start()

        return self.speed

    def pause(self):
        if self.stopped == False:
            self.gui_timer.stop()
            self.enemy_timer.stop()
            self.tower_timer.stop()
            self.wave_timer.stop()
            self.stopped = True
        else:
            self.gui_timer.start()
            self.enemy_timer.start()
            self.tower_timer.start()
            self.wave_timer.start()
            self.stopped = False
