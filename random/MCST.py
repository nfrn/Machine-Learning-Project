import math
import sys
import time
from random import choice


# inspired = started with, but now completely different xD
# inspired in https://jeffbradberry.com/posts/2015/09/intro-to-monte-carlo-tree-search/
# inspired in http://www.baeldung.com/java-monte-carlo-tree-search


class Tree:
    def __init__(self, root):
        self.root = root

    def getRoot(self):
        return self.root

    def setRoot(self,root):
        self.root = root


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
        self.childs.append(child)

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

    def is_root(self):
        return self.parent is None


class MCST:
    def __init__(self, board, time_limit):

        root_state = State(board, None)
        self.tree = Tree(root_state)
        self.time_limit = time_limit
        self.totalplays = 0

    def search_best_move(self):

        searched_games = 0
        begin_time = time.time()

        rootState = self.tree.getRoot()
        self.expand_state(rootState)

        while time.time() - begin_time < self.time_limit:
            next_state = self.get_most_promissing_state(rootState)
            # if next_state.getBoard().is_finished() != 0:
            if not next_state.getBoard().is_finished():
                self.expand_state(next_state)
                # print("State expanded!")

            next_state_childs = next_state.getChilds()

            if len(next_state_childs) > 0:
                random_child_state = choice(next_state_childs)
                sim_state = self.simulate_random_game(random_child_state)
                result = self.state_is_finished(sim_state)
                print("Winner: " + str(result))
                if result != -1:
                    # TODO what if the result is 0 and you have lost?
                    self.backpropagatewin(sim_state, result)
            else:
                sim_state = self.simulate_random_game(next_state)
                result = self.state_is_finished(sim_state)
                print("Winner: " + str(result))
                if result != -1:
                    # TODO what if the result is 0 and you have lost?
                    self.backpropagatewin(sim_state, result)

            searched_games += 1

        print("Searched: " + str(searched_games) + "games.")
        # print("Timed elapsed: " + str(time.time() - begin_time))

        best_move, best_state = self.get_current_best_move()

        self.tree.setRoot(best_state)

        return best_move.get_org().get_pos()[0], best_move.get_org().get_pos()[1], best_move.get_dir()

    def get_most_promissing_state(self, state):

        if len(state.getChilds()) == 0:
            # print("FINAL: Picked state with move " + str(state.getBoard().get_last_move()))
            return state

        else:
            next_state = self.get_state_max_uct(state)
            return self.get_most_promissing_state(next_state)

    def get_state_max_uct(self, state):

        child_states = state.getChilds()

        value = 0
        best_state = child_states[0]
        for state in child_states:
            value2 = self.calculate_uct_value(self.totalplays, state.getwins(), state.getplays())
            if value2 > value:
                value = value2
                best_state = state

        # print("Picked uct move " + str(best_state.getBoard().get_last_move()) + " with uct value of " + str(value))

        return best_state

    def calculate_uct_value(self, total_plays, node_win, node_plays):
        if node_plays == 0:
            return sys.maxsize
        value = ((float(node_win) / node_plays) + 1.41 * math.sqrt(math.log((float(total_plays)) / node_plays)))
        return value

    def simulate_random_game(self, state):
        current_state = state

        while not current_state.getBoard().is_finished():
            current_board = current_state.getBoard()
            possible_moves = current_board.get_free_edges()
            chosen_move = choice(list(possible_moves))

            next_board = copy.deepcopy(current_board)
            next_board.add_edge(chosen_move)

            next_state = State(next_board, current_state)
            current_state.addChilds(next_state)

            current_state = copy.deepcopy(next_state)

        return current_state

    def state_is_finished(self,state):
        current_board = state.getBoard()
        if current_board.is_finished():
            rows = current_board.get_rows()
            cols = current_board.get_columns()
            half_possible_moves = float((rows + 1) * cols) + (rows * (cols + 1)) / 2
            states_played = self.backpropagate_get_winner(state)
            winner = 0
            if states_played > half_possible_moves:
                winner = 1
            return winner
        return -1

    def expand_state(self, state):
        current_board = copy.deepcopy(state.getBoard())
        possible_moves = current_board.get_free_edges()

        for move in possible_moves:
            next_board = copy.deepcopy(current_board)
            next_board.add_edge(move)
            next_state = State(next_board, state)
            state.addChilds(next_state)

    def get_current_best_move(self):
        root_state = self.tree
        next_states = root_state.getRoot().getChilds()
        win_per = 0
        best_state = next_states[0]
        for state in next_states:
            if state.getwins() > 0 and state.getplays() > 0:
                print("Found state with wins.")
                win_per2 = max(float(state.getwins()) / state.getplays())
                if win_per2 > win_per:
                    print("Found best move.")
                    best_state = state
                    win_per = win_per2
        best_move = best_state.getBoard().get_last_move()
        print("Picked move " + str(best_move) + " with win percentage of " + str(win_per))
        return best_move, best_state

    def backpropagatewin(self, state, winner):

        state.inc_plays()
        self.totalplays += 1
        if state.getBoard().get_player == winner:
            state.inc_wins()

        if not state.getParent().is_root():
            self.backpropagatewin(state.getParent(), winner)

    def backpropagate_get_winner(self, state):
        if state.is_root():
            return 0

        else:
            if state.getBoard().get_player() == 1:
                return 1 + self.backpropagate_get_winner(state.getParent())

            else:
                return 0 + self.backpropagate_get_winner(state.getParent())
