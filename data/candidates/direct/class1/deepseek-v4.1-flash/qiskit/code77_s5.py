# EVAL_META: task_id=77, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit

def circuit_from_probability_dist(probability_dist):
    keys = list(probability_dist.keys())
    if not keys:
        return QuantumCircuit(1, 1)

    if all(isinstance(k, str) for k in keys):
        n = max(len(k) for k in keys)
        def to_index(k):
            return int(k.zfill(n), 2)
    else:
        max_key = max(int(k) for k in keys)
        n = max(1, max_key.bit_length())
        def to_index(k):
            return int(k)

    dim = 2 ** n
    statevector = np.zeros(dim, dtype=complex)
    total = sum(probability_dist.values())

    for key, prob in probability_dist.items():
        idx = to_index(key)
        statevector[idx] = np.sqrt(prob / total)

    qc = QuantumCircuit(n)
    qc.initialize(statevector, range(n))
    qc.measure_all()
    return qc
