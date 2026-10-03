# EVAL_META: task_id=77, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit

def circuit_from_probability_dist(probability_dist):
    if not probability_dist:
        qc = QuantumCircuit(1, 1)
        qc.measure(0, 0)
        return qc

    keys = list(probability_dist.keys())
    if all(isinstance(k, str) for k in keys):
        n = max(len(k) for k in keys)
        def to_index(k):
            return int(k.zfill(n), 2)
    elif all(isinstance(k, int) for k in keys):
        max_val = max(keys)
        n = max(1, max_val.bit_length())
        def to_index(k):
            return k
    else:
        str_keys = [str(k) for k in keys]
        n = max(len(k) for k in str_keys)
        def to_index(k):
            return int(str(k).zfill(n), 2)

    dim = 1 << n
    vec = np.zeros(dim, dtype=complex)
    for k, p in probability_dist.items():
        idx = to_index(k)
        if 0 <= idx < dim:
            vec[idx] = np.sqrt(max(0.0, p))

    norm = np.linalg.norm(vec)
    if norm > 0:
        vec /= norm

    qc = QuantumCircuit(n, n)
    qc.initialize(vec, range(n))
    qc.measure(range(n), range(n))
    return qc
