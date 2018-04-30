from board import Board
import numpy as np
if __name__ == "__main__":
    b = Board(6, 6)
    state = b.init_representation()
    moves = b.legal_plays(state)

    for move in moves:
        print("BEGIN_________________")
        print("Move:" + str(move))

        r,c,o = b.translate_to_coord(move)
        print(" ROW:" + str(r) + " COL: " + str(c) + " ORI: " + o)

        new_move = b.translate_to_move(r, c, o)
        print("Move:" + str(new_move))
        print("END_________________")

    state = np.arra
    b.winner()