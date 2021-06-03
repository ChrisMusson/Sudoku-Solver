import sys
from PyQt5.QtWidgets import *
from main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow(window_w=1000, window_h=750, grid_size=740, btn_size=25)
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
