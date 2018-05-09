import os
import logging
import argparse
import pandas
import sys

logger = logging.getLogger(__name__)
filename = "stats.csv"

def test_win_rate(rows, columns, timelimit, nb_games):
    f = open(filename, "w+")
    f.write("timelimit,rows,columns,winner\n")
    f.close()

    for x in range(nb_games):
        os.system('python dotsandboxescompete.py ws://127.0.0.1:8081 ws://127.0.0.1:8082 --rows {} --cols {} --timelimit {}'.format(rows, columns, timelimit))
    stats = pandas.read_csv("stats.csv", delimiter=',')

    print(list(stats))
    nb_games = stats.shape[0]
    nb_wins = stats[stats["winner"] == 1].shape[0]
    nb_draws = stats[stats["winner"] == 0].shape[0]
    print("Win rate for agent 1: " + str(nb_wins/nb_games * 100) + "%.")
    print("Draw rate: " + str(nb_draws/nb_games * 100) + "%.")


def main(argv=None):
    parser = argparse.ArgumentParser(description='Calculate win rate of agent 1 in x games')
    parser.add_argument('--verbose', '-v', action='count', default=0, help='Verbose output')
    parser.add_argument('--quiet', '-q', action='count', default=0, help='Quiet output')
    parser.add_argument('--cols', '-c', type=int, default=2, help='Number of columns')
    parser.add_argument('--rows', '-r', type=int, default=2, help='Number of rows')
    parser.add_argument('--timelimit', '-t', type=float, default=0.5, help='Time limit per request in seconds')
    parser.add_argument('--nb_games', '-g', type=int, default=50, help='The number of games to be simulated')
    # parser.add_argument('agents', nargs=2, metavar='AGENT', help='Websockets addresses for agents')
    args = parser.parse_args(argv)

    logger.setLevel(max(logging.INFO - 10 * (args.verbose - args.quiet), logging.DEBUG))
    logger.addHandler(logging.StreamHandler(sys.stdout))

    # start_competition(args.agents[0], args.agents[1], args.rows, args.cols, args.timelimit)
    test_win_rate(args.rows, args.cols, args.timelimit, args.nb_games)

if __name__ == "__main__":
    sys.exit(main())

