import random
import csv
import script_stats
import baseline_3.dotsandboxesagent_mcst as agent
import os
import threading

filename = "generated_weights.csv"
nb_games = 5
nb_variations = 5
min_size = 3
size_limit = 20
min_time_limit = 0.25
max_time_limit = 1.5


def generator():
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=1)
        writer.writerow(['rows', 'cols', 'time_limit', 'nb_chain_weight', 'avg_chain_weight', 'max_chain_weight', 'winrate', 'drawrate'])

        for x in range(nb_variations):
            print('Testing variation :' + str(x))
            rows = random.randint(min_size, size_limit)
            cols = random.randint(min_size, size_limit)
            time_limit = random.uniform(min_time_limit, max_time_limit)
            nb_chain_weight = random.uniform(0, 2)
            avg_chain_weight = random.uniform(0, 2)
            max_chain_weight = random.uniform(0, 2)

            # agent.main('8081 -w {} {} {}'.format(nb_chain_weight, avg_chain_weight, max_chain_weight))
            # If you do this you get an error that has to do with the directory you are running in.
            os.system(
                'python baseline_3/dotsandboxesagent_mcst.py 8081 -w {} {} {}'.format(nb_chain_weight, avg_chain_weight, max_chain_weight)
            )
            os.system(
                'python baseline_3/dotsandboxesagent_mcst.py 8082 -w 1 1 1')

            # winrate, drawrate = script_stats.test_win_rate(rows, cols, time_limit, nb_games)
            # writer.writerow([rows, cols, time_limit, nb_chain_weight, avg_chain_weight, max_chain_weight, winrate, drawrate])

            t1 = threading.Thread(target=agent.main, name="Agent 1", args=(8081, nb_chain_weight, avg_chain_weight, max_chain_weight))
            t1.daemon = True
            t1.start()

            t2 = threading.Thread(target=agent.main, name="Agent 1", args=(8081, nb_chain_weight, avg_chain_weight, max_chain_weight))
            t2.daemon = True
            t2.start()
    csvfile.close()


if __name__ == "__main__":
    # example get_squares_open(3,3,[1,0,1 ,1,0,1,1 ,1,1,0 ,0,0,1,0, 0,1,1 ,0,0,1,1 ,0,0,0 ])
   #get_features(3,3,[1,1,1                    ,1,0,0,1
                    #1,1,0
                    #0,0,0,1, 1,1,1 ,0,0,0,0 ,0,0,0 ])
    generator()
