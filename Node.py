
from WCircuit import WCircuit
from BinWState import BinWState


class Node:
    amount = 0
    prev_data = ''

    # noise_model = 0
    # coupling_map = 0
    backend = 0

    def __init__(self, data, level, stats):
        self.children = []
        self.data = data
        self.stats = stats
        self.level = level

        self.size = len(stats)

    def __str__(self):
        return self.prev_data + ' ' + str(self.amount)

    def sample(self, type):

        if type == 'quantum':
            w_circuit = WCircuit(self.stats[self.level])
            w_circuit.build_circuit()
            # w_circuit.noise_model = self.noise_model  # noise model
            # w_circuit.coupling_map = self.coupling_map  # topology
            w_circuit.backend = self.backend

            # loop until valid value is obtained
            # while True:
            try:
                counts = w_circuit.sample_circuit(shots=self.amount, simulator=True)
                # break
            except ValueError:
                counts = {}

        else:
            binary_w = BinWState(self.stats[self.level])
            counts = binary_w.sample(size=self.amount)

        # circ = w_cir(self.stats[self.level])
        # counts = sample_circuit(circ, shots=self.amount)

        return counts

    def update_stats(self):
        prev_sample = self.data
        pos = -1

        for i in range(self.size):
            if prev_sample[i] == '1':
                pos = i

        for j in range(self.level, self.size, 1):

            aux = self.stats[j][pos]
            self.stats[j][pos] = 0

            for i in range(self.size):
                if aux == 1:
                    self.stats[j][i] = 0
                else:
                    self.stats[j][i] = self.stats[j][i] / (1 - aux)

                # normalization
                if self.stats[j][i] >= 1.0:
                    self.stats[j][i] = 1.0

    def isleaf(self):
        return len(self.children) == 0
