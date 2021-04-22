from qiskit import QuantumCircuit, Aer, execute, transpile
import numpy as np
from qiskit import IBMQ
import operator
from qiskit.providers.aer import QasmSimulator


class WCircuit:

    circuit = 0
    noise_model = 0
    coupling_map = 0

    counts = 0
    backend = 0

    def __init__(self, statistics):
        self.stats = statistics

    def build_circuit(self):

        # prob_amp = np.sqrt(1/n) all have the same prob of occurrence
        n = len(self.stats)

        list_probs_aux = np.sqrt(self.stats)
        rot_ang = 2 * np.arccos(list_probs_aux[0])

        qc_w = QuantumCircuit(n)

        # probability redistribution
        qc_w.ry(rot_ang, 0)

        for i in range(1, n - 1):
            if 1 - (sum(self.stats[:i])) < 0:
                comp_amp = np.sqrt(0)
            else:
                comp_amp = np.sqrt(1 - (sum(self.stats[:i])))

            # outliers bugs
            if comp_amp == 0:
                rot_ang = 0
            else:
                if list_probs_aux[i] / comp_amp >= 1:  # bug: 1.00000001. arcccos [-1,1]
                    rot_ang = 2 * np.arccos(1)
                else:
                    rot_ang = 2 * np.arccos(list_probs_aux[i] / comp_amp)

            qc_w.cry(rot_ang, i - 1, i)

        # state reshuffling
        for i in range(n - 1, 0, -1):
            qc_w.cx(i - 1, i)

        qc_w.x(0)
        qc_w.measure_all()

        self.circuit = qc_w

    def sample_circuit(self, shots, simulator=True):

        # using simulator or quantum IBM computer
        if simulator:

            if self.backend != 0:
                # 1000 shots to extract probabilities

                aux = QasmSimulator.from_backend(self.backend)
                new_circ_lv0 = transpile(self.circuit, backend=aux, optimization_level=0)
                result = execute(new_circ_lv0,
                                 backend=aux,
                                 shots=1000).result()
                count = result.get_counts(new_circ_lv0)

                # normalization
                possible = valid_solutions(self.stats)
                self.counts = re_build_counts(possible, shots, count)

            else:
                # raise Exception('Backend was not initialized in W_state_opt')
                backend = Aer.get_backend('qasm_simulator')
                result = execute(self.circuit, backend=backend, shots=shots).result()
                resul = result.get_counts(self.circuit)

                possible = valid_solutions(self.stats)
                self.counts = re_build_counts(possible, shots, resul)

        else:
            provider = IBMQ.load_account()
            IBMQ.get_provider(hub='ibm-q')
            backend = provider.get_backend('ibmq_vigo')
            result = execute(self.circuit, backend=backend, shots=shots).result()

            self.counts = result.get_counts(self.circuit)

            raise Exception('Using backend vigo')

        # print(self.stats, self.counts, shots)

        return self.counts


def produce_string(length, pos):
    string = ''
    for i in range(length):
        if i == pos:
            string = string + '1'
        else:
            string = string + '0'
    return string[::-1]


def valid_solutions(stats):
    resul = []
    for i in range(len(stats)):
        if stats[i] > 0.0:
            resul.append(produce_string(len(stats), i))
    return resul


def re_build_counts(possible, size, counts):
    dic = {}
    suma = 0

    for i in possible:
        if i in counts.keys():
            suma = suma + counts[i]

    for i in possible:
        if i in counts.keys():
            dic[i] = int((counts[i] / suma) * size)

    if sum(dic.values()) < size:
        dif = size - sum(dic.values())
        # print(possible, size, counts, dic)
        mx = max(dic.items(), key=operator.itemgetter(1))[0]  # add to the maximum the rests
        dic[mx] = dic[mx] + dif

    # delete the keys whose values == 0
    for key in list(dic.keys()):
        if dic[key] == 0:
            del dic[key]

    return dic
