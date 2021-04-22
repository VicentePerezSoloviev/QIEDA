
from Node import Node
import copy
import pandas as pd


class PLS:

    nodes_list = []
    # noise_model = 0
    # coupling_map = 0
    backend = 0

    def __init__(self, statistics, type):
        self.stats = statistics
        self.N = len(statistics)
        self.type = type

    def sampling(self, shots):
        root = Node('root', level=0, stats=copy.deepcopy(self.stats))
        # root.noise_model = self.noise_model
        # root.coupling_map = self.coupling_map
        root.backend = self.backend
        root.amount = shots
        self.nodes_list = [root]

        for nod in self.nodes_list:  # depth loop

            if nod.level < self.N and nod.size > 0:
                # if nod.amount > 0:
                counts = nod.sample(self.type)
                # print(counts, nod.amount)

                for key in list(counts.keys()):  # width loop
                    aux = Node(key[::-1], nod.level + 1, stats=copy.deepcopy(nod.stats))

                    # aux.noise_model = self.noise_model
                    # aux.coupling_map = self.coupling_map
                    aux.backend = self.backend

                    aux.amount = counts[key]
                    aux.prev_data = nod.prev_data + key[::-1]
                    if nod.level < self.N - 1:
                        aux.update_stats()

                    # print('>', aux.prev_data, aux.stats)
                    nod.children.append(copy.deepcopy(aux))
                    self.nodes_list.append(copy.deepcopy(aux))

    def print_solutions(self):
        for nod in self.nodes_list:
            if nod.isleaf():
                print(nod)

    def return_sols(self):
        sols = pd.DataFrame(columns=['string', 'amount'])
        for nod in self.nodes_list:
            if nod.isleaf():
                if len(nod.prev_data) == self.N**2:
                    sols = sols.append({'string': nod.prev_data, 'amount': nod.amount}, ignore_index=True)

        return sols
