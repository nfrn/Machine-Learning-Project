import random
import csv
import script_stats
import subprocess
import time

filename = "generated_weights3.csv"
nb_games = 20
nb_variations = 10
min_size = 3
size_limit = 20
min_time_limit = 0.25
max_time_limit = 1.0
duration = 3600*7

def generator():
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=1)
        writer.writerow(['rows', 'cols', 'time_limit', 'nb_chain_weight',
                         'avg_chain_weight', 'max_chain_weight',
                         'winrate', 'drawrate'])

        subprocess.Popen('python baseline_3/dotsandboxesagent_mcst.py -q 8081')
        begin = time.time()
        x = 0
        while time.time() - begin < duration:
            r, c, tl, ncw, acw, mcw = get_vars()
            print('Testing variation: ' + str(x) + " with stats {} {} {} {} {} {}".format(r, c, tl, ncw, acw, mcw))

            proc2 = subprocess.Popen('python baseline_3/dotsandboxesagent_mcst.py -q 8082 -w {} {} {}'.format(ncw, acw, mcw))

            wrate, drate = script_stats.test_win_rate(r, c, tl, nb_games)
            writer.writerow([r, c, tl, ncw, acw, mcw, wrate, drate])
            proc2.kill()
            x += 1

    csvfile.close()

def get_vars():
    rows = random.randint(min_size, size_limit)
    cols = random.randint(min_size, size_limit)
    time_limit = random.uniform(min_time_limit, max_time_limit)
    nb_chain_weight = random.uniform(0, 2)
    avg_chain_weight = random.uniform(0, 2)
    max_chain_weight = random.uniform(0, 2)

    return rows, cols, time_limit, nb_chain_weight, avg_chain_weight, max_chain_weight

if __name__ == "__main__":
    generator()
