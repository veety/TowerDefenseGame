import sys, time, json
from PyQt5.QtWidgets import QApplication
from gui import GUI
from board import *
from globals import *
from enemy import *
from coordinates import *
from timer import *
from tower import Tower
import logging


def main():
    board=gameBoard()
    global app
    app = QApplication(sys.argv)
    gui=GUI(board,squareSize)

    timer=Timer(gameSpeed,gui,board)
    sys.exit(app.exec_())



if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    main()