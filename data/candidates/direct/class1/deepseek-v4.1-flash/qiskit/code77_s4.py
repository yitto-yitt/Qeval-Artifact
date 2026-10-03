# EVAL_META: task_id=77, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit

def circuit_from_probability_dist(probability_dist):
    if not probability_dist:
        return QuantumCircuit(0)
    first_key = next(iter(probability_dist))
    if isinstance(first_key, str):
        n = len(first_key)
    else:
        max_key = max(probability_dist.keys())
        n = max(1, max_key.bit_length()) if max_key >= 0 else 1
    dim = 2 ** n
    state = np.zeros(dim, dtype=complex)
    for key, prob in probability_dist.items():
        if isinstance(key, str):
            idx = int(key.strip(), 2)
        else:
            idx = int(key)
        if 0 <= idx < dim:
            state[idx] = np.sqrt(prob)
    norm = np.linalg.norm(state)
    if norm > 0:
        state = state / norm
    qc = QuantumCircuit(n)
    qc.initialize(state)
    qc.measure_all()
    return qc
