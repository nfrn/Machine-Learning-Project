from board import Board
import random
import csv
import numpy as np
import sys

NUMBEROFGAMES=50
SIZELIMIT = 30
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

def expand_chains(chains,rows,cols,state):
    expand = False
    for chain in chains:
        last_square = chain[-1]

        last_square_number = last_square[0]
        last_square_cuts = last_square[1]

        neighbors = get_neighbors(last_square_number,rows,cols)

        for ori,box in neighbors:
            for square, cuts in chain:
                if square == box:
                    neighbors.remove([ori,box])
                    break

        #print(neighbors)

        for neighbor in neighbors:

            neighbor_values = get_square_values(neighbor[1],cols,state)[0]
            numberofcuts = sum(neighbor_values)

            #check if neighbors expand a chain, if yes return expand = True
            if neighbor[0] == 1 and (last_square_cuts[0] == neighbor_values[3]== False) and numberofcuts==2:
                #print("a")
                #print(last_square_cuts)
                #print(neighbor_values)
                #print(neighbor[1])
                chain.append([neighbor[1], neighbor_values])
                expand=True
            if neighbor[0] == 2 and (last_square_cuts[2] == neighbor_values[1]== False) and numberofcuts==2:
                #print("b")
                #print(last_square_cuts)
                #print(neighbor_values)
                #print(neighbor[1])
                chain.append([neighbor[1], neighbor_values])
                expand=True

            if neighbor[0] == 3 and (last_square_cuts[3] == neighbor_values[0]== False) and numberofcuts==2:
                #print("c")
                #print(last_square_cuts)
                #print(neighbor_values)
                #print(neighbor[1])
                chain.append([neighbor[1], neighbor_values])
                expand=True

            if neighbor[0] == 4 and (last_square_cuts[1] == neighbor_values[2]== False) and numberofcuts==2:
                #print("d")
                #print(last_square_cuts)
                #print(neighbor_values)
                #print(neighbor[1])
                chain.append([neighbor[1], neighbor_values])
                expand=True

    return chains, expand


def convert_state(state):
    number = 0
    for x in range(len(state)):
        number += x*10 * state[x]
    return number

def get_features(rows, cols, state):
    chains = create_chains(rows,cols,state)

    expand = True
    count = 0
    while expand and count < 5:
        newchains,expand = expand_chains(chains,rows,cols,state)
        count+=1
        chains = newchains[:]
    if len(chains)==0:
        return 0,0
    value = max(len(chain) for chain in chains)
    return len(chains), value

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
                max_size_chain, number_of_chains = get_features(rows, cols, state[1:])
                #print(5)
                writer.writerow([convert_state(state[1:]), rows, cols, max_size_chain, number_of_chains])
                #print(6)
    csvfile.close()



if __name__ == "__main__":
    # example get_squares_open(3,3,[1,0,1 ,1,0,1,1 ,1,1,0 ,0,0,1,0, 0,1,1 ,0,0,1,1 ,0,0,0 ])
   #get_features(3,3,[1,1,1                    ,1,0,0,1
                    #1,1,0
                    #0,0,0,1, 1,1,1 ,0,0,0,0 ,0,0,0 ])
    generator()

