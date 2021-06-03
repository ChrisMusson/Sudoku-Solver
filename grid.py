from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from utils import get_border_sizes


class SudokuCell(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        font = self.font()
        font.setPointSize(32)
        self.setFont(font)
        self.setMaxLength(1)
        self.setAlignment(Qt.AlignCenter)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)
        self.setAutoFillBackground(True)


class SudokuGrid(QWidget):
    def __init__(self, grid_size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_size = grid_size
        self.setFixedSize(self.grid_size, self.grid_size)

        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        for i in range(9):
            for j in range(9):
                new_cell = SudokuCell(objectName=f"C{i}{j}")
                b = get_border_sizes(i, j, 6, 1)
                new_cell.setStyleSheet(
                    "QLineEdit {{border-style: solid; border-width: {}px {}px {}px {}px}}".format(*b))
                self.layout.addWidget(new_cell, i, j)