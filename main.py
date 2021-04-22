
from EDA import EDA
from TravellingSalesmanProblem import TSP
import pickle
import matplotlib.pyplot as plt
# from qiskit import IBMQ
# from qiskit.providers.aer.noise import NoiseModel


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


tsp = TSP("./datasets/datasetcorto_10")
tsp.load_data()

N = tsp.size()
init = initial_stats(N)

# from qiskit.test.mock import FakeJohannesburg

eda = EDA(init, 50, tsp, 0.5, 40, 40, type='quantum')
# eda.backend = FakeJohannesburg()
best_individual, best_cost, history_cost = eda.run()

print(best_cost, best_individual)
rel_list = relative_list(history_cost)

plt.plot(list(range(len(history_cost))), history_cost)
plt.savefig("./images/QEDA_history.png")

plt.figure()
plt.plot(list(range(len(rel_list))), rel_list)
plt.savefig("./images/QEDA_history_rel.png")

'''
with open('eda.class', 'wb') as eda_file:
    pickle.dump(eda, eda_file)
'''

