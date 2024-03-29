import csv
import random
import sys

from board import Board

NUMBEROFGAMES=200
SIZELIMIT = 25
FILENAME = 'stateToFeatures2.csv'


def get_neighbors(square_number,row, cols):
    total = row * cols
    neighbor = []
    if (square_number//cols == (square_number-1)//cols) and square_number-1 >= 0 and square_number-1 < total:
        neighbor.append([4,square_number-1])
    if (square_number//cols == (square_number+1)//cols) and square_number+1 >=0 and square_number+1 <total:
        neighbor.append([2, square_number+1])
    if square_number + cols < total:
        neighbor.append([3,square_number + cols])
    if square_number - cols >= 0:
        neighbor.append([1,square_number - cols])
    return neighbor

def get_square_values(square, cols, state):
    x1 = square // cols
    y = square % cols

    index = x1 * (cols + cols + 1) + y

    # print("Square:" + str(x+1))
    # print("index:" + str(index))

    list = []

    value1 = state[index] != 0
    value2 = state[index + cols] != 0
    value3 = state[index + cols + 1] != 0
    value4 = state[index + cols + cols + 1] != 0

    list.append(value1)
    list.append(value2)
    list.append(value3)
    list.append(value4)

    square = []

    count = 0
    for ele in list:
        if ele:
            count += 1
            square.append(True)
        else:
            square.append(False)

    return square, count


def convert_neighbor(x):
    if x ==1:
        return 3,0
    if x==2:
        return 1,2
    if x==3:
        return 0,3
    if x==4:
        return 2,1

def get_squares_open(row, cols, state):
    total_squares = row * cols
    squares = []
    for x in range(total_squares):

        square, count = get_square_values(x, cols, state)

        if count == 3:
            squares.append([x,square])
    return squares

def create_chains(rows, cols, state):
    squares = get_squares_open(rows, cols, state)
    chains = []
    for x in range(len(squares)):
        square_number = squares[x][0]
        neighbors = get_neighbors(square_number, rows, cols)
        for x2 in neighbors:
            values = get_square_values(x2[1],cols,state)
            numberofcuts = sum(values[0])
            #print(x2)
            if x2[0] == 1 and (squares[x][1][0] == values[0][3] == False) and numberofcuts==2:
                chains.append([squares[x],[x2[1],values[0]]])

            if x2[0] == 2 and (squares[x][1][2] == values[0][1] == False) and numberofcuts==2:
                chains.append([squares[x],[x2[1],values[0]]])

            if x2[0] == 3 and (squares[x][1][3] == values[0][0] == False) and numberofcuts==2:
                chains.append([squares[x],[x2[1],values[0]]])

            if x2[0] == 4 and (squares[x][1][1] == values[0][2] == False) and numberofcuts==2:
                chains.append([squares[x],[x2[1],values[0]]])

    return chains

def expand_chains(chains,rows,cols,state, closed_chains):
    expand = False
    for chain in chains:
        last_square = chain[-1]

        last_square_number = last_square[0]
        last_square_cuts = last_square[1]

        neighbors = get_neighbors(last_square_number,rows,cols)

        #        print(neighbors)
        for square, cuts in chain:
            for [ori, box] in neighbors:
                if square == box:
                    neighbors.remove([ori,box])


        #print(neighbors)

        for neighbor in neighbors:

            neighbor_values = get_square_values(neighbor[1],cols,state)[0]
            numberofcuts = sum(neighbor_values)

            #check if neighbors expand a chain, if yes return expand = True
            if neighbor[0] == 1 and (last_square_cuts[0] == neighbor_values[3]== False):
                if numberofcuts==2:
                    chain.append([neighbor[1], neighbor_values])
                    expand = True
                if numberofcuts==3:
                    chain.append([neighbor[1], neighbor_values])
                    closed_chains.append(chain)
                    chains.remove(chain)
            if neighbor[0] == 2 and (last_square_cuts[2] == neighbor_values[1]== False):
                if numberofcuts==2:
                    chain.append([neighbor[1], neighbor_values])
                    expand = True
                if numberofcuts==3:
                    chain.append([neighbor[1], neighbor_values])
                    closed_chains.append(chain)
                    chains.remove(chain)

            if neighbor[0] == 3 and (last_square_cuts[3] == neighbor_values[0]== False):
                if numberofcuts==2:
                    chain.append([neighbor[1], neighbor_values])
                    expand = True
                if numberofcuts==3:
                    chain.append([neighbor[1], neighbor_values])
                    closed_chains.append(chain)
                    chains.remove(chain)
            if neighbor[0] == 4 and (last_square_cuts[1] == neighbor_values[2]== False):
                if numberofcuts==2:
                    chain.append([neighbor[1], neighbor_values])
                    expand = True
                if numberofcuts==3:
                    chain.append([neighbor[1], neighbor_values])
                    closed_chains.append(chain)
                    chains.remove(chain)

    return chains, closed_chains, expand

def get_combinations(chains):
    combinations = []
    for chain in chains:
        for chain1 in chains:
            if (not (chain,chain1) in combinations) and  (not (chain1,chain) in combinations):
                combinations.append((chain,chain1))

    return combinations




def merge_chains(chains, rows,cols,state, closedchains):
    list_of_combinations = get_combinations(chains)
    for (chain,chain2) in list_of_combinations:
        if chain != chain2:
            pair_chain = [chain,chain2]
            #print(pair_chain)
            last_square0 = pair_chain[0][-1]
            last_square_number0 = last_square0[0]
            last_square_cuts0 = last_square0[1]

            neighbors0 = get_neighbors(last_square_number0, rows, cols)

            for ori, box in neighbors0:
                for square, cuts in pair_chain[0]:
                    if square == box:
                        neighbors0.remove([ori, box])
                        break

            last_square1 = pair_chain[1][-1]
            last_square_number1 = last_square1[0]
            last_square_cuts1 = last_square1[1]

            neighbors1 = get_neighbors(last_square_number1, rows, cols)

            for ori, box in neighbors1:
                for square, cuts in pair_chain[1]:
                    if square == box:
                        neighbors1.remove([ori, box])
                        break

            for neighbor0 in neighbors0:
                for neighbor1 in neighbors1:
                    if neighbor0[1]==neighbor1[1]:
                        neighbor_values = get_square_values(neighbor0[1], cols, state)[0]
                        numberofcuts = sum(neighbor_values)
                        if numberofcuts == 2:
                            box0, nei0 = convert_neighbor(neighbor0[0])
                            box1, nei1 = convert_neighbor(neighbor1[0])

                            if (last_square_cuts0[box1]==neighbor_values[nei0]==False) and \
                                    (last_square_cuts1[box0]==neighbor_values[nei1]==False):
                                "chains remove A and B"
                                # print("merge")
                                if pair_chain[0] in chains:
                                    chains.remove(pair_chain[0])
                                if pair_chain[1] in chains:
                                    chains.remove(pair_chain[1])
                                "chains add A+B"
                                merged = pair_chain[0] + pair_chain[1] + [[neighbor0[1], neighbor_values]]
                                #print(pair_chain[0])
                                #print(pair_chain[1])
                                #print("merged")
                                closedchains.append(merged)
                                break
                                #print("merged")
    return chains, closedchains


def convert_state(state, cols):
    number = 0
    for x in range(len(state)):
        if state[x] == 0:
            continue
        row, col, ori = translate_to_coord(cols, x+1)
        number += row*col
    return number


def translate_to_coord(cols, move):
    move2 = move - 1

    row = move2 // (cols * 2 + 1)
    col = move2 % (cols * 2 + 1)

    # move = 2 + (row * (self.cols * 2 + 1)) + cols
    # move = 2 + (row * (self.cols * 2 + 1)) + cols + self.cols

    if col < cols:
        return row, col, "h"

    else:
        col -= cols
        return row, col, "v"


def get_features(rows, cols, state):
    chains = create_chains(rows,cols,state)
    closed_chains = []
    expand = True
    # print("nb", end=":")
    while expand:
        chains, closed_chains, expand = expand_chains(chains,rows,cols,state,closed_chains)
        chains, closed_chains = merge_chains(chains, rows, cols, state, closed_chains)
    if len(chains)==0:
        return 0,0,0
    # print(".")
    chains = chains + closed_chains

    max_length = max(len(chain) for chain in chains)
    avg = sum(len(chain) for chain in chains)/len(chains)
    return len(chains), avg, max_length

def generator():
    with open(FILENAME, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=1)

        for x in range(NUMBEROFGAMES):
            rows = random.randint(3, SIZELIMIT)
            cols = random.randint(3, SIZELIMIT)
            print("Game:" + str(x) + " Rows:" + str(rows) + " Cols:" + str(cols))
            sys.stdout.flush()

            board = Board(rows,cols)
            state = board.init_representation()

            while not board.is_finished(state):
                #print(1)
                moves = board.legal_plays(state)
                #print(2)
                new_state = board.next_state(state,random.choice(moves))
                #print(3)
                state = new_state[:]
                #print(4)
                number_of_chains, average, max_size_chain = get_features(rows, cols, state[1:])
                #print(5)
                #print(str(number_of_chains)+ ":" +  str(average) + ":" + str(max_size_chain))
                writer.writerow([convert_state(state[1:], cols), rows, cols, number_of_chains,average,max_size_chain])
                #print(6)
    csvfile.close()


if __name__ == "__main__":
    generator()