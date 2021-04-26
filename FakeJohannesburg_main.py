
from EDA import EDA
from TravellingSalesmanProblem import TSP
from qiskit.test.mock import FakeJohannesburg


def initial_stats(size):
    aux = []
    for i in range(size):
        aux.append([1/size] * size)

    return aux


def relative_list(history):
    relative_history = []
    best = 999999999999999999
    for i in range(len(history_cost)):
        if history_cost[i] < best:
            relative_history.append(history_cost[i])
            best = relative_history[i]
        else:
            relative_history.append(best)

    return relative_history


tsp = TSP("./datasets/datasetcorto_05")
tsp.load_data()

M = 40
N = tsp.size()

# EDA execution
for i in range(M):
    history_cost = []
    init = initial_stats(N)

    eda = EDA(init, 50, tsp, 0.5, 40, 40, type='quantum')
    eda.backend = FakeJohannesburg()

    best_individual, best_cost, history_cost = eda.run(output=False)
    print(i, best_cost, history_cost)

    """with open('./experiments/04/experiment04_' + num_ciudades + '_FakeJohannesburg.txt', 'a') as f:
        for item in history_cost:
            f.write("%s " % item)
        f.write("\n")"""
