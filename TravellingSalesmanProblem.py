
import numpy as np


class TSP:

    adjacency_matrix = 0

    def __init__(self, file):
        self.data = file

    def load_data(self):
        f = open(self.data)
        info = []
        num_lineas = 0
        try:
            for linea in f:
                ciudad = []
                for palabra in linea.split(' '):
                    ciudad.append(float(palabra))
                info.append(ciudad)
                num_lineas += 1
        finally:
            f.close()

        matriz = np.zeros((len(info), len(info)))
        for i in range(len(info) - 1):
            for j in range(i + 1, len(info)):
                coste = np.sqrt((info[i][1] - info[j][1]) ** 2 + (info[i][2] - info[j][2]) ** 2)
                matriz[i][j] = coste
                matriz[j][i] = coste

        self.adjacency_matrix = matriz
        # print(matriz)

    def evaluate_solution(self, solution):
        cost = 0

        for i in range(len(solution) - 1):
            cost = cost + self.adjacency_matrix[solution[i]][solution[i+1]]

        return cost

    def size(self):
        return len(self.adjacency_matrix)

