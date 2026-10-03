# EVAL_META: task_id=77, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit

def circuit_from_probability_dist(probability_dist):
    if not probability_dist:
        return QuantumCircuit(0)
    bitstrs = list(probability_dist.keys())
    n = len(bitstrs[0])
    dim = 2 ** n
    statevector = np.zeros(dim, dtype=complex)
    for bitstring, prob in probability_dist.items():
        index = int(bitstring, 2)
        statevector[index] = np.sqrt(float(prob))
    qc = QuantumCircuit(n)
    qc.initialize(statevector, range(n))
    qc.measure_all()
    return qc
