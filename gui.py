from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import  QColor, QBrush
from PyQt5.QtCore import Qt
from board import *
from coordinates import Coordinates

class GUI(QtWidgets.QMainWindow):
    def __init__(self,board,square_size):
        super().__init__()
        self.setCentralWidget(QtWidgets.QWidget())
        self.horizontal=QtWidgets.QHBoxLayout()
        self.centralWidget().setLayout(self.horizontal)
        self.board=board
        self.square_size=square_size
        self.init_window()
        self.add_board_grid_items()



    def add_board_grid_items(self):
        for i in range(self.board.get_width()):
            for j in range(self.board.get_height()):
                coordinates=Coordinates(i,j)
                ispath=self.board.get_square(coordinates).is_path()
                if ispath:
                    qp = QBrush(QColor(150, 75, 0), Qt.SolidPattern)
                    rectangle = QGraphicsRectItem(self.square_size * coordinates.get_x(),
                                                  self.square_size * coordinates.get_y(), self.square_size,
                                                  self.square_size)
                    rectangle.setBrush(qp)
                else:
                    qp = QBrush(QColor(30, 130, 30), Qt.SolidPattern)
                    rectangle = QGraphicsRectItem(self.square_size * coordinates.get_x(),
                                                  self.square_size * coordinates.get_y(), self.square_size,
                                                  self.square_size)
                    rectangle.setBrush(qp)
                self.scene.addItem(rectangle)

    def init_window(self):
        self.setGeometry(300,300,800,800)
        self.setWindowTitle('Tower Defense')
        self.show()

        self.scene=QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0,0,700,700)

        self.view=QtWidgets.QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.show()
        self.horizontal.addWidget(self.view)