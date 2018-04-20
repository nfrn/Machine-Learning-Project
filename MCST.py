from board import Board
from random import choice
import time
import sys
import math
#inspired = started with, but now completely different xD
#inspired in https://jeffbradberry.com/posts/2015/09/intro-to-monte-carlo-tree-search/
#inspired in http://www.baeldung.com/java-monte-carlo-tree-search


class Tree:

    def __init__(self, root):
        self.root = root

    def getRoot(self):
        return self.root


class State:

    def __init__(self, board, parent):
        self.board = board
        self.parent = parent
        self.wins = 0
        self.plays = 0
        self.childs = []
        self.explored = False

    def __eq__(self, other):
        return (self.board == other.board) and (self.parent == other.parent)

    def getBoard(self):
        return self.board

    def getParent(self):
        return self.parent

    def getChilds(self):
        return self.childs

    def addChilds(self, child):
        self.childs.append( child)

    def getwins(self):
        return self.wins

    def getplays(self):
        return self.plays

    def inc_wins(self):
        self.wins += 1

    def inc_plays(self):
        self.plays += 1

    def setWinRate(self, win_rate):
        self.win_rate = win_rate

    def explored(self):
        self.explored = True

    def is_explored(self):
        return self.explored

class UCT:

    def __init__(self, total_plays, node_win, node_plays):
        self.total_plays = total_plays
        self.node_win = node_win
        self.node_plays = node_plays

    def calculate_uct_value(self):
        if self.node_plays == 0:
            return sys.maxsize
        "1.41 = sqrt(2)"
        value = ( float(self.node_win)/ self.node_plays) +  + 1.41 * math.sqrt(math.log( (float(self.total_plays)) / self.node_plays));
        return value


class MCST:
    def __init__(self, board, time_limit):

        root_state = State(board, 0)
        self.tree = Tree(root_state)
        self.time_limit = time_limit

    def search_best_move(self):

        searched_games = 0
        begin_time = time.time()

        while time.time() - begin_time < self.time_limit :
            self.select_move_uct()
            self.expand_random_move()
            searched_games += 1

        print("Searched: " + str(searched_games) + "games.")
        print("Timed elapsed: " + str(time.time() - begin_time))

        move = self.get_current_best_move()

        return move

    def select_move_uct():



    def expand_random_move(self):
        current_state = self.tree.getRoot()

        current_board = current_state.getBoard()

        possible_moves = current_board.get_free_edges()
        chosen_move = choice(list(possible_moves))

        next_board = current_board
        next_board.add_edge(chosen_move)
        next_state = State(next_board, current_state)

        if next_state not in current_state.getChilds():
            current_state.addChilds(next_state)

        if next_board.is_finished():
            winner = next_board.get_winner()
            rows = next_board.get_rows()
            cols = next_board.get_cols()
            half_possible_moves = float((rows + 1) * cols) + (rows * (cols + 1)) / 2
            states_played = self.backpropagate_get_winner(next_state)

            if states_played > half_possible_moves:
                winner = 1
            else:
                winner = 0

            self.backpropagatewin(next_state, winner)


    def get_current_best_move(self):

        root_state = self.tree
        next_states = root_state.getRoot().getChilds()

        max_win_percentage, best_state = ((max(float(state.getwins) / state.getplays), state) for state in next_states)
        best_move = best_state.get_last_move()

        print("Picked move " + best_move + " with win percentage of " + max_win_percentage)

        return best_move

    def backpropagatewin(self,state, winner):

        state.inc_plays()

        if state.getBoard().get_player == winner :
            state.inc_wins()

        if state.getParent != 0:
            self.backprogratewin(state.getParent(), winner)


    def backpropagate_get_winner(self,state):

        if state.getParent != 0:

            if state.getBoard().get_player()== 1:
                return 1 + self.backpropagate_get_winner(state.getParent())

            else:
                return 0 + self.backpropagate_get_winner(state.getParent())





