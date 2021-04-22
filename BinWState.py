from numpy.random import multinomial


class BinWState:

    stats = []

    def __init__(self, statistics):
        self.stats = normalization(statistics)

    def sample(self, size):
        dic = {}
        for i in range(size):
            sampling = list(multinomial(1, self.stats, size=1)[0])
            s2 = list2str_inv(sampling)
            dic = add2dict(dic, s2)
        return dic


def to_w_state(lista):
    return lista.index(max(lista))


def list2str_inv(lista):
    string = [str(lista[i]) for i in range(len(lista))]
    separator = ''
    string = separator.join(string)
    return string[::-1]


def add2dict(dictionary, item):
    if item in list(dictionary.keys()):
        dictionary[item] = dictionary[item] + 1
    else:
        dictionary[item] = 1
    return dictionary


def normalization(lista):
    suma = sum(lista)
    for i in range(len(lista)):
        if lista[i] >= 1.0:
            lista = [0.0] * len(lista)
            lista[i] = 1.0
        elif lista[i] <= 0.0:
            lista[i] = 0.0
        else:
            lista[i] = lista[i]/suma
    return lista
