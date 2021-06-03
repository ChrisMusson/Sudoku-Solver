from mip import BINARY, Model, xsum


def solve(data):
    numbers = [[[0 for i in range(9)] for j in range(9)] for k in range(9)]

    for i, n in enumerate(data["givens"]):
        if int(n) != 0:
            numbers[i // 9][i % 9][int(n) - 1] = 1

    kropki, xv = "0"*144, "0"*144
    for i, char in enumerate(data["orthog_inters"]):
        if char == "0":
            continue
        elif char in ["W", "B"]:
            kropki = kropki[:i] + char + kropki[i+1:]
        elif char in ["X", "V"]:
            xv = xv[:i] + char + xv[i+1:]
        else:
            print("Something has gone wrong.")

    m = Model()

    # define 3D boolean matrix where k defines the value
    x = [[[m.add_var(var_type=BINARY)
           for j in range(9)]
          for i in range(9)]
         for k in range(9)]

    # fixed values constraints
    for i in range(9):
        for j in range(9):
            for k in range(9):
                if numbers[i][j][k] == 1:
                    m += x[i][j][k] == 1

    # exactly 1 value per cell
    for i in range(9):
        for j in range(9):
            m += xsum(x[i][j][k] for k in range(9)) == 1

    # numbers 1-9 in each row
    for i in range(9):
        for k in range(9):
            m += xsum(x[i][j][k] for j in range(9)) == 1

    # numbers 1-9 in each column
    for j in range(9):
        for k in range(9):
            m += xsum(x[i][j][k] for i in range(9)) == 1

    # numbers 1-9 in each 3x3 region
    for i2 in range(3):
        for j2 in range(3):
            for k in range(9):
                m += xsum(x[i][j][k]
                          for i in range(i2 * 3, i2 * 3 + 3)
                          for j in range(j2 * 3, j2 * 3 + 3)
                          ) == 1

    # numbers 1-9 on each long diagonal
    if data["bool_diag"]:
        for k in range(9):
            m += xsum(x[i][i][k] for i in range(9)) == 1
            m += xsum(x[i][8 - i][k] for i in range(9)) == 1

    # no cells containing the same value within one king's move of each other
    if data["bool_ak"]:
        king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                      (0, 1), (1, -1), (1, 0), (1, 1)]
        for i in range(9):
            for j in range(9):
                for move in king_moves:
                    if i + move[0] not in list(range(9)) or j + move[1] not in list(range(9)):
                        continue
                    else:
                        for k in range(9):
                            m += x[i][j][k] + \
                                x[i + move[0]][j + move[1]][k] <= 1

    # no cells containing the same value within one knight's move of each other
    if data["bool_an"]:
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                        (1, -2), (1, 2), (2, -1), (2, 1)]
        for i in range(9):
            for j in range(9):
                for move in knight_moves:
                    if i + move[0] not in list(range(9)) or j + move[1] not in list(range(9)):
                        continue
                    else:
                        for k in range(9):
                            m += x[i][j][k] + \
                                x[i + move[0]][j + move[1]][k] <= 1

    # no cells containing consecutive digits orthogonally adjacent to each other
    if data["bool_ac"]:
        orthog_adjacent = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        for i in range(9):
            for j in range(9):
                for move in orthog_adjacent:
                    if i + move[0] not in list(range(9)) or j + move[1] not in list(range(9)):
                        continue
                    else:
                        for k in range(9):
                            if k < 8:
                                m += x[i][j][k] + x[i + move[0]
                                                    ][j + move[1]][k + 1] <= 1
                            if k > 0:
                                m += x[i][j][k] + x[i + move[0]
                                                    ][j + move[1]][k - 1] <= 1

    # White circle between cells -> difference of 1. Black circle between cells -> quotient of 2.
    # should always be 144 chars, "0"*144 if kropki is not involved.
    if kropki != "0"*144:
        all_tuples = [(x+1, y+1) for x in range(9) for y in range(9)]
        poss_b = [(i+1, j+1) for i in range(9) for j in range(9) if (i+1)/(j+1) in [0.5, 2]]
        poss_w = [(i+1, j+1) for i in range(9) for j in range(9) if abs(i-j) == 1]
        poss_bw = list(set(poss_b + poss_w))
        for idx, char in enumerate(kropki):
            a = idx // 17
            b = idx % 17
            if char != "0":
                for t in all_tuples:
                    if (char == "W" and t not in poss_w) or (char == "B" and t not in poss_b):
                        # on a horizontal line. Cells involved will be (a, b - 8) and (a + 1, b - 8)
                        if b >= 8:
                            m += x[a][b-8][t[0] - 1] + x[a+1][b-8][t[1] - 1] <= 1
                        # on a vertical line. Cells involved will be (a, b) and (a, b + 1)
                        else:
                            m += x[a][b][t[0] - 1] + x[a][b+1][t[1] - 1] <= 1

            else:
                if data["bool_neg_krop"]:
                    for t in poss_bw:
                        if b >= 8:
                            m += x[a][b-8][t[0] - 1] + x[a+1][b-8][t[1] - 1] <= 1
                        else:
                            m += x[a][b][t[0] - 1] + x[a][b+1][t[1] - 1] <= 1

    if xv != "0"*144:
        all_tuples = [(x+1, y+1) for x in range(9) for y in range(9)]
        poss_x = [(i+1, j+1) for i in range(9) for j in range(9) if i + j + 2 == 10]
        poss_v = [(i+1, j+1) for i in range(9) for j in range(9) if i + j + 2 == 5]
        poss_xv = list(set(poss_x + poss_v))
        for idx, char in enumerate(xv):
            a = idx // 17
            b = idx % 17
            if char != "0":
                for t in all_tuples:
                    if (char == "X" and t not in poss_x) or (char == "V" and t not in poss_v):
                        if b >= 8:  # horizontal
                            m += x[a][b-8][t[0] - 1] + x[a+1][b-8][t[1] - 1] <= 1
                        else:  # vertical
                            m += x[a][b][t[0] - 1] + x[a][b+1][t[1] - 1] <= 1
            else:
                if data["bool_neg_xv"]:
                    for t in poss_xv:
                        if b >= 8:
                            m += x[a][b-8][t[0] - 1] + x[a+1][b-8][t[1] - 1] <= 1
                        else:
                            m += x[a][b][t[0] - 1] + x[a][b+1][t[1] - 1] <= 1

    # TODO: Implement killer sudoku into the GUI
    # if killer:
    #     layout = inst.killer_layout
    #     regions = [tuple((int(r.strip()[2 * k]), int(r.strip()[2 * k + 1]))
    #                      for k in range(int((len(r.strip()) - 0.25) // 2))) for r in layout]
    #     totals = [int(term.strip()[-2:]) if len(term.strip()) %
    #               2 == 0 else int(term.strip()[-1:]) for term in layout]

    #     # add region constraints
    #     for n, region in enumerate(regions):
    #         # no repeated digits in a region
    #         for k in range(9):
    #             m += xsum(x[cell[0]][cell[1]][k] for cell in region) <= 1
    #         # if the total is given, ensure the cells sum to that number
    #         if totals[n] > 0:
    #             m += xsum(xsum((k + 1) * x[cell[0]][cell[1]][k]
    #                            for cell in region) for k in range(9)) == totals[n]

    # TODO: Implement thermo sudoku into the solver and the GUI

    m.optimize()
    return x
