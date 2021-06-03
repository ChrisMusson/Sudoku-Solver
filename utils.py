from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def get_border_sizes(i, j, large, small):
    """
    returns the desired border sizes given a SudokuCell's i,j coordinates in
    the grid layout. this seems like such a stupid and long-winded way
    to do it but it should kind of work
    """
    if i % 3 == 0:
        if i == 0:
            top = large
        else:
            top = large // 2
        bottom = small
    elif i % 3 == 2:
        if i == 8:
            bottom = large
        else:
            bottom = large // 2
        top = small
    else:
        top = small
        bottom = small

    if j % 3 == 0:
        if j == 0:
            left = large
        else:
            left = large // 2
        right = small
    elif j % 3 == 2:
        if j == 8:
            right = large
        else:
            right = large // 2
        left = small
    else:
        left = small
        right = small

    return (top, right, bottom, left)

