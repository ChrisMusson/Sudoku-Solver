from PyQt5.QtWidgets import *
from intersections import *
from sudoku import solve
from grid import SudokuGrid
from tooltips import tooltips


class MainWindow(QMainWindow):
    def __init__(self, window_w, window_h, grid_size, btn_size):
        super().__init__()
        self.window_w = window_w
        self.window_h = window_h
        self.grid_size = grid_size
        self.btn_size = btn_size
        self.orthogonal_intersections_shown = True
        self.diagonal_intersections_shown = True
        self.initUi()

    def initUi(self):
        self.setWindowTitle("Sudoku Solver")
        self.setGeometry(100, 100, self.window_w, self.window_h)

        widget = QWidget(self)
        self.setCentralWidget(widget)

        hor_box = QHBoxLayout()
        widget.setLayout(hor_box)

        self.frame = QFrame(widget)
        self.frame.setFixedSize(self.grid_size, self.grid_size)

        self.grid = SudokuGrid(self.grid_size, self.frame, objectName="grid")
        hor_box.addWidget(self.frame)
        self.show()  # must be done now to allow future calculations of co-ords for QLineInputs

        add_orthogonal_intersections(self)
        add_diagonal_intersections(self)

        ver_box = QVBoxLayout()
        hor_box.addLayout(ver_box)
        ver_box.addStretch()

        checkboxes = {
            "Anti-consecutive": "bool_ac",
            "Anti-king": "bool_ak",
            "Anti-knight": "bool_an",
            "Diagonal": "bool_diag",
            "Negative Kropki": "bool_neg_krop",
            "Negative XV": "bool_neg_xv"
        }

        for k, v in checkboxes.items():
            cb = QCheckBox(k, objectName=v)
            cb.setToolTip(tooltips[v])
            ver_box.addWidget(cb)

        ver_box.addItem(QSpacerItem(0, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))

        toggle_orthogonal_intersections_btn = QPushButton("Toggle Orthogonal Intersection Points", self)
        toggle_orthogonal_intersections_btn.clicked.connect(lambda: toggle_orthogonal_intersections(self))
        ver_box.addWidget(toggle_orthogonal_intersections_btn)
        toggle_orthogonal_intersections(self)

        toggle_diagonal_intersections_btn = QPushButton("Toggle Diagonal Intersection Points", self)
        toggle_diagonal_intersections_btn.clicked.connect(lambda: toggle_diagonal_intersections(self))
        ver_box.addWidget(toggle_diagonal_intersections_btn)
        toggle_diagonal_intersections(self)

        ver_box.addItem(QSpacerItem(0, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))

        clear_numbers_btn = QPushButton("CLEAR NUMBERS", self)
        clear_numbers_btn.clicked.connect(self.clear_numbers)
        ver_box.addWidget(clear_numbers_btn)

        clear_intersections_btn = QPushButton("CLEAR INTERSECTIONS", self)
        clear_intersections_btn.clicked.connect(lambda: clear_all_intersections(self))
        ver_box.addWidget(clear_intersections_btn)

        solve_btn = QPushButton("SOLVE", self)
        solve_btn.clicked.connect(self.show_solution)
        ver_box.addWidget(solve_btn)

        ver_box.addStretch()

        self.show()

    def find_solution(self):
        givens = "".join([self.findChild(QLineEdit, f"C{i}{j}").text() or "0" for i in range(9) for j in range(9)])
        orthog_inters = "".join([self.findChild(QLineEdit, f"OI{i:03d}").text() or "0" for i in range(144)])

        bool_ac = self.findChild(QCheckBox, "bool_ac").isChecked()
        bool_ak = self.findChild(QCheckBox, "bool_ak").isChecked()
        bool_an = self.findChild(QCheckBox, "bool_an").isChecked()
        bool_diag = self.findChild(QCheckBox, "bool_diag").isChecked()

        bool_neg_krop = self.findChild(QCheckBox, "bool_neg_krop").isChecked()
        bool_neg_xv = self.findChild(QCheckBox, "bool_neg_xv").isChecked()

        data = {
            "givens": givens,
            "orthog_inters": orthog_inters,
            "bool_ac": bool_ac,
            "bool_ak": bool_ak,
            "bool_an": bool_an,
            "bool_diag": bool_diag,
            "bool_neg_krop": bool_neg_krop,
            "bool_neg_xv": bool_neg_xv
        }
        print(data)  # TODO: DELETE

        return solve(data)

    def show_solution(self):
        x = self.find_solution()

        sol = ""  # TODO: DELETE
        try:
            for i in range(9):
                for j in range(9):
                    for k in range(9):
                        if x[i][j][k].x >= 0.99:
                            sol += str(k+1)
                            self.findChild(
                                QLineEdit, f"C{i}{j}").setText(str(k+1))

            print(sol)  # TODO: DELETE

        except TypeError:
            print("\n\nNo solution could be found.\n\n")  # TODO: alert user that it failed, a pop up perhaps

    def clear_numbers(self):
        for i in range(9):
            for j in range(9):
                self.findChild(QLineEdit, f"C{i}{j}").setText("")

    def update_css(self, s):
        sender = self.sender()
        if s == "":
            if self.intersections_shown:
                sender.setStyleSheet(
                    "QLineEdit {border-radius: 0; border-width: 1px; border-style: solid}")
            else:
                sender.setStyleSheet(
                    "QLineEdit {border-style: none; background-color: transparent}")
        elif s.upper() == "V":
            sender.setStyleSheet(
                f"QLineEdit {{border-radius: {self.btn_size // 2}; font-size: 24px; font-weight:500}}")
            sender.setText("V")
        elif s.upper() == "X":
            sender.setStyleSheet(
                f"QLineEdit {{border-radius: {self.btn_size // 2}; font-size: 24px; font-weight:500}}")
            sender.setText("X")
        elif s.upper() == "W":
            sender.setStyleSheet(
                f"QLineEdit {{border-radius: {self.btn_size // 2}; border-width: 1px; border-style: solid; color:white}}")
            sender.setText("W")
        elif s.upper() == "B":
            sender.setStyleSheet(
                f"QLineEdit {{border-radius: {self.btn_size // 2}; border-width: 1px; border-style: solid; background-color: black}}")
            sender.setText("B")
        else:
            sender.setText("")