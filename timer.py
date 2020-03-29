from globals import *
from PyQt5 import QtCore
#from gui import GUI

class Timer():
    def __init__(self,gameSpeed,gui,board):
        self.gui=gui
        self.board=board
        self.stopped=False
        self.gui.timer=self

        self.gui_timer=QtCore.QTimer()
        self.gui_timer.timeout.connect(self.gui.update_enemies)
     #   self.gui_timer.timeout.connect(self.gui.delete_enemy_graphics_items)
        self.gui_timer.timeout.connect(self.board.move_enemies)
        self.gui_timer.start(10)

        self.tower_timer=QtCore.QTimer()
        self.tower_timer.timeout.connect(self.board.tower_updater)
        self.tower_timer.timeout.connect(self.gui.update_towers)
        self.tower_timer.start(100)

        self.wave_timer=QtCore.QTimer()
        self.wave_timer.timeout.connect(self.board.wave_manager)
        self.wave_timer.start(1000)

    def pause(self):
        if self.stopped == False:
            self.gui_timer.stop()
            self.tower_timer.stop()
            self.wave_timer.stop()
            self.stopped = True
        else:
            self.gui_timer.start()
            self.tower_timer.start()
            self.wave_timer.start()
            self.stopped = False
