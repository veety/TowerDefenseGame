from PyQt5.QtWidgets import QApplication
from gui import GUI
from board import *
from timer import *
import logging
import sys


def main():
    board=gameBoard()
    global app
    app = QApplication(sys.argv)
    gui=GUI(board)
    timer=Timer(gui,board)
    sys.exit(app.exec_())

if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    main()