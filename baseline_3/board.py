import numpy as np
from hashlib import sha1
from numpy import all, array, uint8
import collections

class hashable(object):

    def __init__(self, wrapped, tight=False):
        r'''Creates a new hashable object encapsulating an ndarray.

            wrapped
                The wrapped ndarray.

            tight
                Optional. If True, a copy of the input ndaray is created.
                Defaults to False.
        '''
        self.__tight = tight
        self.__wrapped = array(wrapped) if tight else wrapped
        self.__hash = int(sha1(wrapped.view(uint8)).hexdigest(), 16)

    def __eq__(self, other):
        return all(self.__wrapped == other.__wrapped)

    def __hash__(self):
        return self.__hash

    def unwrap(self):
        r'''Returns the encapsulated ndarray.

            If the wrapper is "tight", a copy of the encapsulated ndarray is
            returned. Otherwise, the encapsulated ndarray itself is returned.
        '''
        if self.__tight:
            return array(self.__wrapped)

        return self.__wrapped


class Board:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    # INTERFACE FOR MCST

    def init_representation(self):
        state = np.zeros((1 + (self.rows * self.cols * 2) + self.rows + self.cols), dtype=np.int8)
        state[0] = 1
        return state

    def current_player(self, state):
        return state.item(0)

    def next_state(self, state, move):
        new_state = np.copy(state)
        currentplayer = state.item(0)
        row, col, ori = self.translate_to_coord(move)
        new_state[move] = currentplayer

        if self.is_box(new_state, row, col, ori):
            new_state[0] = currentplayer
        else:
            new_state[0] = self.update_player(currentplayer)

        return new_state

    def legal_plays(self, state):
        plays = np.where(state == 0)[0]
        return plays

    def is_finished(self, state):
        plays = np.where(state == 0)[0]
        if len(plays) == 0:
            return True
        return False

    def register_state(self, state, row, cols, ori, player):
        new_state = np.copy(state)

        move = self.translate_to_move(row, cols, ori)
        new_state[move] = player

        if self.is_box(new_state, row, cols, ori):
            new_state[0] = player
        else:
            new_state[0] = self.update_player(player)

        return new_state, move

    # Utility Functions
    def winner(self, state):
        board = state[1:]
        win = collections.Counter(board).most_common()[0][0]
        return win

    def translate_to_move(self,row,cols,ori):
        move = (row * (self.cols * 2 + 1)) + cols + 1
        if ori == "v":
            move += self.cols
        return move

    def translate_to_coord(self, move):
        move2 = move - 1

        rows = move2 // (self.cols * 2 + 1)
        cols = move2 % (self.cols * 2 + 1)

        # move = 2 + (row * (self.cols * 2 + 1)) + cols
        # move = 2 + (row * (self.cols * 2 + 1)) + cols + self.cols

        if cols < self.cols:
            return rows, cols, "h"

        else:
            cols -= self.cols
            return rows, cols, "v"

    def update_player(self, player):
        return 2*player % 3

    def is_box(self, new_state, row, col, ori):
        move = self.translate_to_move(row, col, ori)
        cols = self.cols
        if ori == "h":
            if row < self.rows:
                if new_state.item(move + cols) > 0 and new_state.item(move + cols + 1) > 0 and new_state.item(move + (2 * cols) + 1) > 0:
                    return True
            if row > 1:
                if new_state.item(move - cols) > 0 and new_state.item(move - cols - 1) > 0 and new_state.item(move - (2 * cols) - 1) > 0:
                    return True
        elif ori == "v":
            if col < self.cols:
                if new_state.item(move + 1) > 0 and new_state.item(move - cols) > 0 and new_state.item(move + cols + 1) > 0:
                    return True
            if col > 1:
                if new_state.item(move - 1) > 0 and new_state.item(move + cols) > 0 and new_state.item(move - cols - 1) > 0:
                    return True
        return False
