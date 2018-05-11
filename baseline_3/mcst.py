import time
import numpy as np
import math
from random import choice
from board import hashable
from board import Board
from sklearn.externals import joblib

MAX_PREDICTOR_FILENAME = "Models/max_chain_length_classifier.sav"
COUNT_PREDICTOR_FILENAME = "Models/nb_chains_classifier.sav"
AVG_PREDICTOR_FILENAME = "Models/avg_chain_length_classifier.sav"

timing = False


class Mcst:

    def __init__(self, board, time_limit, weights, cmm, ccm, cam):

        init1 = time.time()
        self.time_limit = time_limit
        self.board = board  # Simulation class
        self.last_state = (1, self.board.init_representation())
        self.next_states = []     # (MOVE, STATE)
        self.visited_states = []  # (MOVE, STATE)

        self.wins = {}    # (PLAYER, hash(STATE))
        self.plays = {}   # (PLAYER, hash(STATE))
        self.weights = weights

        loadm1 = time.time()
        self.chain_max_model = cmm
        loadm2 = time.time()
        self.chain_count_model = ccm
        loadm3 = time.time()
        self.chain_avg_model = cam
        loadm4 = time.time()
        if timing:
            print("Mcst initialisation time: {}".format(loadm1-init1))
            print("Max chain model load time: {}".format(loadm2 - loadm1))
            print("Count chain model load time: {}".format(loadm3 - loadm2))
            print("Average chain model load time: {}".format(loadm4 - loadm3))


    def clear(self):
        self.board = Board(self.board.rows, self.board.cols)
        self.last_state = (1, self.board.init_representation())
        self.next_states = []  # (MOVE, STATE)
        self.visited_states = []  # (MOVE, STATE)

    def search_move(self):
        begin_time = time.time()
        simulated_games = 0

        current_state = self.last_state
        possible_moves = self.board.legal_plays(current_state[1])

        self.next_states = self.expand_state(current_state[1])
        self.visited_states = list(self.next_states)

        player1 = self.board.current_player(current_state[1])

        if possible_moves.shape[0] == 0:
            return -1

        while time.time() - begin_time < self.time_limit * 0.9:
            self.simulate_random_game(player1)
            simulated_games += 1



        # print("Simulated games: " + str(simulated_games))

        state, move, r, c, o = self.get_best_move(self.next_states)
        self.last_state = (move, state)
        #print("Diference: {}".format((time.time() - begin_time)-self.time_limit))
        return r.item(), c.item(), o

    def expand_state(self, current_state):
        next_states = []
        moves = self.board.legal_plays(current_state)
        for move in moves:
            new_state = self.board.next_state(current_state, move)
            next_states.append((move, new_state))

            player = self.board.current_player(new_state)
            hash_state = hashable(new_state)

            if(player, hash_state) not in self.plays.keys():
                self.plays[(player, hash_state)] = 0
                self.wins[(player, hash_state)] = 0

        return next_states

    def get_best_move(self, next_states):

        best_win = 0
        best_move, best_state = choice(next_states)
        # begin = time.time()
        for move, state in next_states:
            plays = self.plays.get((self.board.current_player(state), hashable(state)), 1)
            if plays != 0:
                wins = self.wins.get((self.board.current_player(state), hashable(state)), 0)
                win = float(wins)/plays
                if win > best_win:
                    best_win = win
                    best_move = move
                    best_state = state
        # print("Time to pick best move: {}".format(time.time() - begin))
        # print("Picked move " + str(best_move) + " with win rate of " + str(best_win))
        r, c, o = self.board.translate_to_coord(best_move)
        return best_state, best_move, r, c, o

    def simulate_random_game(self, player1):
        init1 = time.time()
        state, move = self.uct_selection(self.next_states)
        init2 = time.time()
        player = self.board.current_player(state)
        init3 = time.time()
        states_simulated = list()
        init4 = time.time()
        states_simulated.append((player, hashable(state)))
        init5 = time.time()
        state_copy = np.copy(state)
        # print("Time to init board: {}".format(init5 - init1))
        t = init2 - init1
        # if t > 0.1:
        # print("Time to init uct: {}".format(init2 - init1))
        # print("Time to set player: {}".format(init3 - init2))
        # print("Time to make list: {}".format(init4 - init3))
        # print("Time to append to list: {}".format(init5 - init4))

        finish = time.time()
        while not self.board.is_finished(state_copy):

            next_states = self.expand_state(state_copy)

            # uct = time.time()
            state_copy, move = self.uct_selection(next_states)
            # print("UCT Time: {}".format(time.time()-uct))

            state_hash = hashable(state_copy)
            new_player = self.board.current_player(state_copy)
            states_simulated.append((new_player, state_hash))
        finished = time.time()
        # print("Time to finish board: {}".format(finished-finish))
        winner = self.board.winner(state_copy)
        # EXTRA

        for player, hash_state in states_simulated:
            self.plays[(player, hash_state)] += 1
            if player1 == winner:
                self.wins[(player, hash_state)] += 1
        # print("Time to update tree: {}".format(time.time() - finished))

    def register_other_player_move(self, row, col, ori, player):
        new_state, new_move = self.board.register_state(self.last_state[1], row, col, ori, player)
        self.last_state = (new_move, new_state)

    def uct_selection(self, states):
        b = self.board

        init1 = time.time()
        list_not_played = []
        # TODO niet uitvoeren als alle next states al gevisit zijn.
        for move, state in states:
            if self.plays[(b.current_player(state), hashable(state))] == 0:
                list_not_played.append((state, move))

        init2 = time.time()
        # print("Time to make list: {}".format(init2 - init1))

        if len(list_not_played) > 0:
            return choice(list_not_played)

        init3 = time.time()
        # print("Time to make random choice from unplayed: {}".format(init3 - init2))

        log_total = math.log(
            sum(self.plays[(b.current_player(S), hashable(S))] for p, S in states))

        value, move, state = max(
            ((float(self.wins[(b.current_player(S), hashable(S))]) / self.plays[(b.current_player(S), hashable(S))]) +
             1.4 * math.sqrt(float(log_total) / self.plays[(b.current_player(S), hashable(S))])
             + self.get_prediction_value(S[1:], b.rows, b.cols)
             , p, S)
            for p, S in states)
        init4 = time.time()
        #print("Time to calculate stuff: {}".format(init4 - init3))
        # value, move, state = max(
        #     ((float(self.wins[(self.board.current_player(S), hashable(S))]) / self.plays[(self.board.current_player(S), hashable(S))]) +
        #      1.4 * math.sqrt(float(log_total) / self.plays[(self.board.current_player(S), hashable(S))])
        #      + self.weights[0] * self.chain_count_model.predict([[convert_state(S[1:], self.board.rows, self.board.cols), self.board.rows, self.board.cols]])
        #      + self.weights[1] * self.chain_avg_model.predict([[convert_state(S[1:], self.board.rows, self.board.cols), self.board.rows, self.board.cols,
        #                                                         self.chain_count_model.predict([[convert_state(S[1:], self.board.rows, self.board.cols), self.board.rows, self.board.cols]])]])
        #      + self.weights[2] * self.chain_max_model.predict(
        #         [[convert_state(S[1:], self.board.rows, self.board.cols), self.board.rows, self.board.cols,
        #           self.chain_count_model.predict([[convert_state(S[1:], self.board.rows, self.board.cols), self.board.rows, self.board.cols]]),
        #           self.chain_avg_model.predict([[convert_state(S[1:], self.board.rows, self.board.cols), self.board.rows, self.board.cols,self.chain_count_model.predict([[convert_state(S[1:], self.board.rows, self.board.cols), self.board.rows, self.board.cols]])]])]])
        #      , p, S)
        #     for p, S in states)
        init1 = time.time()
        # print("Selected state with uct value:" + str(value))
        return state, move

    def get_prediction_value(self, state, r, c):
        begin = time.time()
        cstate = convert_state(state, c)
        convert = time.time()
        #print("Time to convert state: {}".format(convert-begin))
        ccpred = self.chain_count_model.predict([[cstate, r, c]])
        avgpred = self.chain_avg_model.predict([[cstate, r, c, ccpred]])
        maxpred = self.chain_max_model.predict([[cstate, r, c, ccpred, avgpred]])
        #print("Time to get predictions: {}".format(time.time() - convert))
        w = self.weights
        return ccpred * w[0] + \
               avgpred * w[1] + \
               maxpred * w[2]


# def convert_state(state):
#     number = 0
#     for x in range(len(state)):
#         if state[x] == 0:
#             continue
#         number += x*10
#     return number

# TODO might get done more efficient by keeping a converted state as well.
def convert_state(state, cols):
    number = 0
    for x in range(len(state)):
        if state[x] == 0:
            continue
        row, col, ori = translate_to_coord(cols, x + 1)
        number += row*col
    return number


def translate_to_coord(cols, move):
    move2 = move - 1

    row = move2 // (cols * 2 + 1)
    col = move2 % (cols * 2 + 1)

    if col < cols:
        return row, col, "h"

    else:
        col -= cols
        return row, col, "v"
