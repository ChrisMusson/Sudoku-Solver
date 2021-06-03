from sudoku import solve


def convert_solution(sol):
    sol_str = ""
    for i in range(9):
        for j in range(9):
            for k in range(9):
                if sol[i][j][k].x >= 0.99:
                    sol_str += str(k+1)
    return sol_str


list_puzz = {
    "https://www.funwithpuzzles.com/2015/04/anti-knight-xv-sudoku.html": {
        "givens": "000000000000000000000000000000400000000000000000002000000000000000000000000000000",
        "orthog_inters": "000V0X0000000X0000000V000000000000V00000V000X000000X00000000000000000000000X00V00000V000000000X0000000X00000000V00000X0000X0000X00000000VX0000V0",
        "bool_ac": False,
        "bool_ak": False,
        "bool_an": True,
        "bool_diag": False,
        "bool_neg_krop": True,
        "bool_neg_xv": False,
        "solution": "859236471362714958417589236283457169594361782671892543738125694925643817146978325"
    },
    "https://sudokumaniacs.com/playgame.php?td=20200728V&co=false": {
        "givens": "000000000000000000000000000000000000000000000000000000000000000000000000000000000",
        "orthog_inters": "0W00W00000BBW000000W00000000W0WB00W00B00WBW000000WB0000000W00000WWW0BW00000000000B000000B0000000W00000000000B0WWW000000WBW00W00000WWW00000BW00W0",
        "bool_ac": False,
        "bool_ak": False,
        "bool_an": False,
        "bool_diag": False,
        "bool_neg_krop": True,
        "bool_neg_xv": False,
        "solution": "354689271182374695769215348691752834845193726273846159527961483436528917918437562"
    }
}
