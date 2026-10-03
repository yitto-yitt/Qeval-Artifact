# EVAL_META: task_id=77, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit

def circuit_from_probability_dist(probability_dist):
    if not probability_dist:
        return QuantumCircuit(1)
    keys = [str(k) for k in probability_dist.keys()]
    n = max(len(k) for k in keys)
    state = np.zeros(2**n, dtype=complex)
    for k, p in probability_dist.items():
        k_str = str(k).zfill(n)
        idx = int(k_str, 2)
        state[idx] = np.sqrt(p)
    norm = np.linalg.norm(state)
    if norm > 0:
        state = state / norm
    qc = QuantumCircuit(n)
    qc.initialize(state, range(n))
    qc.measure_all()
    return qc
