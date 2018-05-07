from board import Board
import random
import csv
import numpy as np

NUMBEROFGAMES=10
SIZELIMIT = 10


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
        print("Square:" + str(square_number))
        neighbors = get_neighbors(square_number, rows, cols)
        print(squares[x][1])
        print(neighbors)
        for x2 in neighbors:
            values = get_square_values(x2[1],cols,state)
            print(values)
            print(squares[x][1])
            if values[1] == 1:
                pass
            # missing other scenarios just looking at right(2)
            if values[1] == 2 and squares[x][1][0] == squares[x][1][3] == values[0][0] == values[0][3]:
                chains.append([squares[x],[x2[1],values[0]]])

            if values[1] == 3:
                pass
            if values[1] == 4:
                pass

    return chains

def expand_chains(chains,rows,cols,state):
    expand = False
    for chain in chains:
        last_square = chain[-1]

        last_square_number = last_square[0]
        last_square_cuts = last_square[1]
        # remove from neighbors the boxes already in the chain.
        #squares_in_chain= []
        #for square, cuts in chain:
         #   squares_in_chain.append(square)

        neighbors = get_neighbors(last_square_number,rows,cols)

        for neighbor in neighbors:

            neighbor_values = get_square_values(neighbor[1],cols,state)[0]
            numberofcuts = sum(neighbor_values)
            print("CUTS:"+ str(numberofcuts))
            #check if neighbors expand a chain, if yes return expand = True
            if neighbor[0] == 1:
                pass
                # missing other scenarios just looking at right(2)
            if neighbor[0] == 2 and last_square_cuts[2] != neighbor_values[2] and numberofcuts==2:
                chain.append([neighbor[1], neighbor_values])
                expand=True

            if neighbor[0] == 3:
                pass
            if neighbor[0] == 4:
                pass

    return chains, expand

def classify_chains(chains):
    return 1,2,3,4,5

def get_features(rows, cols, state):
    chains = create_chains(rows,cols,state)
    print(chains)

    expand = True
    while expand:
        newchains,expand = expand_chains(chains,rows,cols,state)
        chains = newchains[:]

    print(chains)
    total_chains, half_open, closed, prepared, prepared_closed = classify_chains(chains)
    return total_chains, half_open, closed, prepared, prepared_closed


def generator():
    with open('stateToFeatures.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        for x in range(NUMBEROFGAMES):
            rows = random.randint(1, 10)
            cols = random.randint(1, 10)

            board = Board(rows,cols)

            state = board.init_representation()

            total_chains, half_open, closed, prepared, prepared_closed = get_features(rows, cols,state[1:]);

            writer.writerow(state[1:], rows, cols, total_chains, half_open, closed, prepared, prepared_closed)



if __name__ == "__main__":
    # example get_squares_open(3,3,[1,0,1 ,1,0,1,1 ,1,1,0 ,0,0,1,0, 0,1,1 ,0,0,1,1 ,0,0,0 ])
    get_features(3,3,[1,1,1 ,1,0,0,0 ,1,1,1 ,0,0,0,0, 0,0,0 ,0,0,0,0 ,0,0,0 ])


