import time
import numpy as np
import collections
import sys
import math
from random import choice
from board import hashable
from board import Board
from sklearn.externals import joblib

MAX_PREDICTOR_FILENAME = "Models/chain_count.sav"
COUNT_PREDICTOR_FILENAME = "Models/chain_max.sav"


class Mcst:

    def __init__(self, board, time_limit):
        self.time_limit = time_limit
        self.board = board  # Simulation class
        self.last_state = (1, self.board.init_representation())
        self.next_states = [] # (MOVE, STATE)
        self.visited_states = [] # (MOVE, STATE)

        self.wins = {}    # (PLAYER, hash(STATE))
        self.plays = {}   # (PLAYER, hash(STATE))

        self.chain_max_model = joblib.load(MAX_PREDICTOR_FILENAME)
        self.chain_count_model = joblib.load(COUNT_PREDICTOR_FILENAME)

    def clear(self):
        self.board = Board(self.board.rows, self.board.cols)
        self.last_state = (1, self.board.init_representation())
        self.next_states = []  # (MOVE, STATE)
        self.visited_states = []  # (MOVE, STATE)

    def search_move(self):
        print("Dictionary reset: " + str(len(self.plays) == 0))
        begin_time = time.time()
        simulated_games = 0

        current_state = self.last_state
        possible_moves = self.board.legal_plays(current_state[1])

        self.next_states = self.expand_state(current_state[1])
        self.visited_states = list(self.next_states)

        player1 = self.board.current_player(current_state[1])

        if possible_moves.shape[0] == 0:
            print("No possible moves.")
            return -1

        while time.time() - begin_time < self.time_limit:
            self.simulate_random_game(player1)
            simulated_games += 1

        print("Simulated games: " + str(simulated_games))

        state, move, r,c,o = self.get_best_move(self.next_states)
        self.last_state = (move, state)

        return r.item(),c.item(),o

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

    def get_best_move(self,next_states):

        best_win = 0
        best_move, best_state = choice(next_states)

        for move, state in next_states:
            plays = self.plays.get((self.board.current_player(state), hashable(state)), 1)
            if plays != 0:
                wins = self.wins.get((self.board.current_player(state), hashable(state)), 0)
                win = float(wins)/plays
                if win > best_win:
                    best_win = win
                    best_move = move
                    best_state = state

        print("Picked move " + str(best_move) + " with win rate of " + str(best_win))
        r,c,o = self.board.translate_to_coord(best_move)
        return best_state, best_move, r,c,o

    def simulate_random_game(self, player1):

        state, move = self.uct_selection(self.next_states)
        player = self.board.current_player(state)
        states_simulated = list()
        states_simulated.append((player, hashable(state)))

        state_copy = np.copy(state)

        while not self.board.is_finished(state_copy):

            next_states = self.expand_state(state_copy)

            state_copy, move = self.uct_selection(next_states)

            state_hash = hashable(state_copy)
            new_player = self.board.current_player(state_copy)
            states_simulated.append((new_player, state_hash))

        winner = self.board.winner(state_copy)
        # EXTRA

        for player, hash_state in states_simulated:
            self.plays[(player, hash_state)] += 1
            if player1 == winner:
                self.wins[(player, hash_state)] += 1

    def register_other_player_move(self, row, col, ori, player):
        new_state, new_move = self.board.register_state(self.last_state[1], row, col, ori, player)
        self.last_state = (new_move, new_state)



    def uct_selection(self, states):

        list_not_played = []
        # TODO niet uitvoeren als alle next states al gevisit zijn.
        for move, state in states:
            if self.plays[(self.board.current_player(state), hashable(state))] == 0:
                list_not_played.append((state,move))

        if len(list_not_played) > 0:
            return choice(list_not_played)

        log_total = math.log(
            sum(self.plays[(self.board.current_player(S), hashable(S))] for p, S in states))

        value, move, state = max(
            ((float(self.wins[(self.board.current_player(S), hashable(S))]) / self.plays[(self.board.current_player(S), hashable(S))]) +
             1.4 * math.sqrt(float(log_total) / self.plays[(self.board.current_player(S), hashable(S))])
             + self.chain_max_model.predict([[convert_state(S[1:]), self.board.rows, self.board.cols]])

             , p, S)
            for p, S in states)

        # print("Selected state with uct value:" + str(value))
        return state, move


def convert_state(state):
    number = 0
    for x in range(len(state)):
        number += x*10 * state[x]
    return number

