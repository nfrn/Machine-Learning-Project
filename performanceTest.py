import time
import random

def updateplayer1(player):
    new_player = (player + 1) % 2
    if new_player == 0:
        new_player = 2
    return new_player


def updateplayer2(player):
    return 2*player % 3


def compare_update_player():
    print("Comparing update_player function...")
    assert updateplayer1(1) == 2
    assert updateplayer1(2) == 1
    assert updateplayer2(1) == 2
    assert updateplayer2(2) == 1

    begin_2 = time.time()
    for i in range(1000000):
        updateplayer2(1)
        updateplayer2(2)
    end_2 = time.time()
    time2 = end_2 - begin_2

    begin_1 = time.time()
    for i in range(1000000):
        updateplayer1(1)
        updateplayer1(2)
    end_1 = time.time()
    time1 = end_1 - begin_1

    print("Elapsed time for version 1: {} seconds.".format(time1))
    print("Elapsed time for version 2: {} seconds.".format(time2))
    print("Speedup of: {} %\n".format((1.0 - (time2/time1))*100))


def convert_state1(state):
    number = 0
    for x in range(len(state)):
        number += x * 10 * state[x]
    return number


def convert_state2(state):
    number = 0
    for x in range(len(state)):
        if state[x] == 0:
            continue
        number += x * 10
    return number


def compare_convert_state():
    print("Comparing convert_state function...")
    state = [random.choice(range(3)) for _ in range(40000)]

    begin_1 = time.time()
    for i in range(100):
        convert_state1(state)
    end_1 = time.time()
    time1 = end_1 - begin_1

    begin_2 = time.time()
    for i in range(100):
        convert_state2(state)
    end_2 = time.time()
    time2 = end_2 - begin_2

    print("Elapsed time for version 1: {} seconds.".format(time1))
    print("Elapsed time for version 2: {} seconds.".format(time2))
    print("Speedup of: {} %\n".format((1.0 - (time2/time1))*100))


if __name__ == "__main__":
    compare_update_player()
    compare_convert_state()
