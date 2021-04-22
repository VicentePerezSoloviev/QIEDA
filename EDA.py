from ProbabilisticLogicSampling import PLS
import pandas as pd
import ast


class EDA:
    generation = pd.DataFrame(columns=['string', 'amount'])

    best_individual = 0
    best_cost = 99999999999999
    history_cost = []
    best_local = 0
    best_local_cost = 0

    penalization = 9999999

    # noise_model = 0
    # coupling_map = 0
    backend = 0

    def __init__(self, statistics, size_gen, tsp_problem, alpha, it_max, it_dead, type):
        self.stats = statistics
        self.size_gen = size_gen
        self.tsp_problem = tsp_problem
        self.alpha = alpha
        self.trunc_size = int(alpha * size_gen)
        self.it_max = it_max
        self.id_dead = it_dead

        self.history_cost = []

        self.type = type

    def new_generation(self):
        pls = PLS(statistics=self.stats, type=self.type)

        if self.type == 'quantum':
            # pls.noise_model = self.noise_model
            # pls.coupling_map = self.coupling_map
            pls.backend = self.backend

        pls.sampling(shots=self.size_gen)
        self.generation = pls.return_sols()

    def translate_individual(self, string):
        tam = len(self.stats)
        sol = []
        for i in range(tam):
            aux = string[tam * i: tam * (i + 1)]
            pos = 0
            for j in range(tam):
                if aux[j] == '1':
                    pos = j
            sol.append(pos)

        # print(string, sol)

        return sol

    def evaluation(self):
        # evaluation with adjacency matrix
        solutions = list(self.generation['string'])
        self.generation['cost'] = 99999999999
        self.generation['trans'] = 0

        for sol in solutions:
            translation = self.translate_individual(sol)
            cost = self.tsp_problem.evaluate_solution(translation)

            flag = 0
            for i in range(len(self.stats)):
                if i not in translation:
                    flag = flag + 1

            if flag:  # if not all cities in the path, then penalize
                cost = cost + self.penalization * flag

            self.generation.loc[self.generation.string == sol, 'cost'] = cost
            self.generation.loc[self.generation.string == sol, 'trans'] = str(translation)

    def truncation(self):
        # selection of bests solutions
        self.generation = self.generation.sort_values(by=['cost'])
        self.generation['amount_acum'] = self.generation['amount'].cumsum()
        self.generation = self.generation.reset_index()
        del self.generation['index']

        trunc_size = sum(self.generation['amount']) * self.alpha
        self.trunc_size = trunc_size

        aux = 0
        for i in range(len(self.generation)):
            if self.generation.loc[i, 'amount_acum'] >= trunc_size:
                aux = i + 1
                break

        self.generation = self.generation[:aux]
        self.generation.loc[aux - 1, 'amount'] = self.generation.loc[aux - 1, 'amount'] - \
                                                 (self.generation.loc[aux - 1]['amount_acum'] - trunc_size)

        self.generation.loc[aux - 1, 'amount_acum'] = self.generation.loc[aux - 1]['amount_acum'] - \
                                                      (self.generation.loc[aux - 1]['amount_acum'] - trunc_size)

        # self.generation = self.generation.nsmallest(trunc_size, 'cost')

    def update_statistics(self):
        keys = list(self.generation['string'])
        tam_data, string_tam, tam_problem = len(keys), len(self.stats) ** 2, len(self.stats)
        amounts = list(self.generation['amount'])

        for i in range(string_tam):  # string size loop
            tot = 0
            for j in range(tam_data):  # solutions loop
                if keys[j][i] == '1':
                    tot = tot + amounts[j]

            self.stats[i % tam_problem][int(i / tam_problem)] = tot / self.trunc_size

    def run(self, output=True):
        no_improves = 0
        array = []

        for i in range(self.it_max):
            self.new_generation()
            self.evaluation()
            self.truncation()
            self.update_statistics()

            # best individual update
            self.best_local = self.generation.loc[0, 'trans']
            self.best_local_cost = self.generation.loc[0, 'cost']

            if self.best_local_cost < self.best_cost:
                self.best_individual = self.generation.loc[0, 'trans']
                array.append(ast.literal_eval(self.best_individual))
                self.best_cost = self.best_local_cost
                no_improves = 0
            else:
                no_improves = no_improves + 1

            self.history_cost.append(self.best_local_cost)

            if output:
                print('[iteration ', i + 1, ']', self.best_local_cost, self.best_local)

            # print(self.stats)
            # print(self.generation)

            if no_improves == self.id_dead:
                break

        return self.best_individual, self.best_cost, self.history_cost, array
