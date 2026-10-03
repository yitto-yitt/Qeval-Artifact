# EVAL_META: task_id=77, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit

def circuit_from_probability_dist(probability_dist):
    if not probability_dist:
        return QuantumCircuit(0)

    keys = list(probability_dist.keys())
    values = [float(probability_dist[k]) for k in keys]
    if any(v < 0 for v in values):
        raise ValueError("Probabilities must be non-negative")

    total = sum(values)
    if total <= 0:
        raise ValueError("The sum of probabilities must be positive")
    probs = [v / total for v in values]

    if all(isinstance(k, str) and len(k) > 0 and set(k).issubset({'0', '1'}) for k in keys):
        indices = [int(k, 2) for k in keys]
        n = max(len(k) for k in keys)
    else:
        try:
            indices = [int(k) for k in keys]
            if any(idx < 0 for idx in indices):
                raise ValueError
        except (TypeError, ValueError):
            indices = list(range(len(keys)))
            n = max(1, int(np.ceil(np.log2(len(indices)))))
        else:
            n = max(1, int(np.ceil(np.log2(max(indices) + 1))))

    state = np.zeros(2 ** n, dtype=complex)
    combined = {}
    for idx, p in zip(indices, probs):
        if idx < 0 or idx >= 2 ** n:
            raise ValueError("Measurement index out of range")
        combined[idx] = combined.get(idx, 0.0) + p

    for idx, p in combined.items():
        state[idx] = np.sqrt(p)

    norm = np.linalg.norm(state)
    if norm == 0:
        raise ValueError("Invalid probability distribution")
    state = state / norm

    qc = QuantumCircuit(n)
    qc.initialize(state.tolist(), qc.qubits)
    qc.measure_all()
    return qc
