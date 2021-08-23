# Quantum-inspired Estimation of Distribution Algorithm (QIEDA)

This repository contains all the code of the QIEDA approach. The QIEDA es a quantum-inspired evolutionary algorithm 
which exploits the benefits of the circuit model-based quantum computers. It is a hybrid implementation between classical
and quantum programming. Quantum computing principles are used in the reproduction step of the algorithm.

This is the general repository. However, it is planned to add the QIEDA implementation to 
EDAspy package (https://github.com/VicentePerezSoloviev/EDAspy).

QIEDA approach is presented in the IEEE Congress on Evolutionary Computation 2021. It has been applied
to solve the Traveling Salesman Problem (TSP) and compared with other well-known state-of-the-art 
population-based algorithms such as Binary Particle Swarm Optimization, Ant Colony Optimization and Genetic 
algorithms.

## Some interesting results:

TSP datasets used to analyse the behaviour of the QIEDA compared to other algorithms can be found in
https://github.com/VicentePerezSoloviev/QIEDA/tree/master/datasets and were obtained from http://www.math.uwaterloo.ca/tsp/world/countries.html

IBM quantum computers were used and Qiskit (0.16.0) is used for the programming part of the code.

### Quantum noise

Quantum noise is considered in the results. A modified version of the W State quantum circuits is used in
order to be able to set specific probabilities for each of the quantum pure states. In next figure, the difference
between executing the quantum circuit without (a) and with (b) noise can be observed.

![W State histograms](./horizon_hists_wstate.PNG?raw=true "Histogram W State")

### Cost analysis

![Cost analysis](./cost_comparison.png?raw=true "Cost comparison")

Mean best cost for the TSP for different number of cities and
different algorithms: QIEDA executed in the Johannesburg quantum simulator
with noise, QIEDA executed in a quantum simulator without quantum noise,
the non-quantum estimation of distribution algorithm (EDA), particle swarm
optimization (PSO), genetic algorithm (GA), and the ant colony optimization
(ACO).

### Convergence analysis

![Convergence analysis](./convergence_comparison.png?raw=true "Convergence comparison")

Mean convergence for the TSP for different number of cities and
different algorithms: QIEDA executed in the Johannesburg quantum simulator
with noise, QIEDA executed in a quantum simulator without quantum noise,
the non-quantum estimation of distribution algorithm (EDA), particle swarm
optimization (PSO), genetic algorithm (GA), and the ant colony optimization
(ACO).

### Computing topology

Original article also provides a benchmarking of how the topology choice can affect in the execution
time of the QIEDA, and an ideal topology (https://github.com/VicentePerezSoloviev/QIEDA/blob/master/chainbackend.py) is proposed in order to decrease the depth of the quantum circuits.

### Citation

Soloviev, V. P., Bielza, C., & Larrañaga, P. (2021, June). Quantum-Inspired Estimation Of Distribution Algorithm To Solve The Travelling Salesman Problem. In 2021 IEEE Congress on Evolutionary Computation (CEC) (pp. 416-425). IEEE.

@inproceedings{soloviev2021quantum,
  title={Quantum-Inspired Estimation Of Distribution Algorithm To Solve The Travelling Salesman Problem},
  author={Soloviev, Vicente P and Bielza, Concha and Larra{\~n}aga, Pedro},
  booktitle={2021 IEEE Congress on Evolutionary Computation (CEC)},
  pages={416--425},
  year={2021},
  organization={IEEE}
}

 
