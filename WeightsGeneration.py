import random
import csv
import script_stats
import subprocess
import time
import argparse
import sys

# filename = "weights_vs_random.csv"
# nb_games = 10
# # nb_variations = 10
# min_size = 15
# size_limit = 20
# min_time_limit = 0.2
# max_time_limit = 0.4
# duration = 1800

LOGGING = True

def generator(ports, mins, maxs, gpv, mint, maxt, runt, filename):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=1)
        # writer.writerow(['rows', 'cols', 'time_limit', 'nb_chain_weight',
        #                  'avg_chain_weight', 'max_chain_weight',
        #                  'winrate', 'drawrate'])

        proc1 = subprocess.Popen('python random/dotsandboxesagentrandom.py -q {}'.format(ports[1]))
        begin = time.time()
        x = 1
        while time.time() - begin < runt:
            r, c, tl, ncw, acw, mcw = get_vars(mins, maxs, mint, maxt)
            if LOGGING:
                print('Testing variation: ' + str(x) + " with stats {} {} {} {} {} {}".format(r, c, tl, ncw, acw, mcw))

            proc2 = subprocess.Popen('python '
                                     'baseline_3/dotsandboxesagent_mcst.py '
                                     '{} -q -w {} {} {}'.format(ports[0], ncw,
                                                                acw, mcw))
            time.sleep(5)
            wrate, drate = script_stats.test_win_rate(r, c, tl, gpv, ports)
            writer.writerow([r, c, tl, ncw, acw, mcw, wrate, drate])
            csvfile.flush()
            proc2.kill()

            x += 1
            time.sleep(1)
    proc1.kill()
    csvfile.close()

def get_vars(min_size, max_size, min_time_limit, max_time_limit):
    rows = random.randint(min_size, max_size)
    cols = random.randint(min_size, max_size)
    time_limit = random.uniform(min_time_limit, max_time_limit)
    nb_chain_weight = random.uniform(-2, 2)
    avg_chain_weight = random.uniform(-2, 2)
    max_chain_weight = random.uniform(-2, 2)

    return rows, cols, time_limit, nb_chain_weight, avg_chain_weight, max_chain_weight


def main(argv=None):
    parser = argparse.ArgumentParser(description='Simulate games')
    parser.add_argument('ports', nargs=2, type=int)
    parser.add_argument('--min_size', '-min', type=int, default=3)
    parser.add_argument('--max_size', '-max', type=int, default=20)
    parser.add_argument('--games_per_var', '-gpv', type=int, default=10)
    parser.add_argument('--min_timelimit', '-mint', type=float, default=0.1)
    parser.add_argument('--max_timelimit', '-maxt', type=float, default=0.2)
    parser.add_argument('--run_time', '-rt', type=int, default=600)
    parser.add_argument('--filename', '-f', default="weights_vs_random.csv")

    args = parser.parse_args(argv)
    generator(args.ports, args.min_size, args.max_size, args.games_per_var,
              args.min_timelimit, args.max_timelimit, args.run_time,
              args.filename)

if __name__ == "__main__":
    sys.exit(main())
