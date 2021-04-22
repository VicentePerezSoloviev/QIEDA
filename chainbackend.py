
from qiskit.providers.models.backendconfiguration import BackendConfiguration
from qiskit.providers.models.backendproperties import BackendProperties
from datetime import date


class ChainBackend:

    def __init__(self, n_qubits):
        coupling_map = []
        for i in range(n_qubits - 1):
            coupling_map.append([i, i+1])

        self.conf = BackendConfiguration(backend_name='chain_backend',
                                         n_qubits=n_qubits,
                                         basis_gates=['id', 'u1', 'u2', 'u3', 'cx'],
                                         local=True,
                                         open_pulse=False,
                                         max_shots=8000,
                                         coupling_map=coupling_map,
                                         backend_version='-1',
                                         conditional=True,
                                         simulator=False,
                                         gates=[],
                                         memory=True)

        today = date.today()
        d1 = today.strftime("%d/%m/%Y")

        self.props = BackendProperties(backend_name='chain_backend',
                                       backend_version='-1',
                                       last_update_date=d1,
                                       qubits=[],
                                       gates=[],
                                       general=[])

    def configuration(self):
        return self.conf

    def properties(self):
        return self.props
