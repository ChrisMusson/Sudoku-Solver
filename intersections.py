from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


def add_orthogonal_intersections(window):
    for i in range(9):
        for j in range(8):
            next_cell = window.grid.layout.itemAtPosition(i, j + 1).geometry()
            mid = QPoint(next_cell.x(), next_cell.y() + next_cell.height() // 2)
            geom = QRect(mid.x() - window.btn_size // 2, mid.y() - window.btn_size // 2, window.btn_size, window.btn_size)
            box_1 = QLineEdit(window.frame, objectName=f"OI{17*i + j:03d}", maxLength=1, alignment=Qt.AlignCenter, geometry=geom)
            box_1.textEdited.connect(window.update_css)
            box_1.show()

            next_cell = window.grid.layout.itemAtPosition(j + 1, i).geometry()
            mid = QPoint(next_cell.x() + next_cell.width() // 2, next_cell.y())
            geom = QRect(mid.x() - window.btn_size // 2, mid.y() - window.btn_size // 2, window.btn_size, window.btn_size)
            box_2 = QLineEdit(window.frame, objectName=f"OI{17 * (j+1) + i - 9:03d}", maxLength=1, alignment=Qt.AlignCenter, geometry=geom)
            box_2.textEdited.connect(window.update_css)
            box_2.show()


def add_diagonal_intersections(window):
    for i in range(8):
        for j in range(8):
            cell = window.grid.layout.itemAtPosition(i, j).geometry()
            mid = QPoint(cell.x() + cell.width(), cell.y() + cell.height())
            geom = QRect(mid.x() - window.btn_size // 2, mid.y() - window.btn_size // 2, window.btn_size, window.btn_size)
            box = QLineEdit(window.frame, objectName=f"DI{8 * i + j:02d}", alignment=Qt.AlignCenter, geometry=geom)
            box.show()


def clear_orthogonal_intersections(window):
    for num in range(144):
        child = window.findChild(QLineEdit, f"OI{num:03d}")
        child.setText("")
        if window.orthogonal_intersections_shown:
            child.setStyleSheet(
                "QLineEdit {border-radius: 0; border-width: 1px; border-style: solid}")
        else:
            child.setStyleSheet(
                "QLineEdit {border-style: none; background-color: transparent}")


def clear_diagonal_intersections(window):
    for num in range(64):
        child = window.findChild(QLineEdit, f"DI{num:02d}")
        child.setText("")
        if window.diagonal_intersections_shown:
            child.setStyleSheet(
                "QLineEdit {border-radius: 0; border-width: 1px; border-style: solid}")
        else:
            child.setStyleSheet(
                "QLineEdit {border-style: none; background-color: transparent}")


def clear_all_intersections(window):
    clear_orthogonal_intersections(window)
    clear_diagonal_intersections(window)


def toggle_orthogonal_intersections(window):
    for num in range(144):
        child = window.findChild(QLineEdit, f"OI{num:03d}")
        if child.text() == "":
            if window.orthogonal_intersections_shown:
                child.setStyleSheet(
                    "QLineEdit {border-style: none; background-color: transparent}")
            else:
                child.setStyleSheet(
                    "QLineEdit {border-radius: 0; border-width: 1px; border-style: solid}")

    window.orthogonal_intersections_shown = not window.orthogonal_intersections_shown


def toggle_diagonal_intersections(window):
    for num in range(64):
        child = window.findChild(QLineEdit, f"DI{num:02d}")
        if child.text() == "":
            if window.diagonal_intersections_shown:
                child.setStyleSheet(
                    "QLineEdit {border-style: none; background-color: transparent}")
            else:
                child.setStyleSheet(
                    "QLineEdit {border-radius: 0; border-width: 1px; border-style: solid}")

    window.diagonal_intersections_shown = not window.diagonal_intersections_shown
