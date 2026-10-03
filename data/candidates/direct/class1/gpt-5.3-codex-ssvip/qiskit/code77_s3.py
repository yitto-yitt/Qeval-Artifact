# EVAL_META: task_id=77, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np


def circuit_from_probability_dist(probability_dist):
    if not isinstance(probability_dist, dict) or len(probability_dist) == 0:
        raise ValueError("probability_dist must be a non-empty dictionary.")

    keys = list(probability_dist.keys())
    if not all(isinstance(k, str) for k in keys):
        raise ValueError("All measurement keys must be bitstrings.")

    n = len(keys[0])
    if n == 0:
        raise ValueError("Bitstrings must be non-empty.")
    if not all(len(k) == n for k in keys):
        raise ValueError("All bitstrings must have the same length.")
    if not all(set(k).issubset({"0", "1"}) for k in keys):
        raise ValueError("Bitstrings must contain only '0' and '1'.")

    probs = np.zeros(2**n, dtype=float)
    total = 0.0
    for bitstr, p in probability_dist.items():
        p = float(p)
        if p < -1e-12:
            raise ValueError("Probabilities must be non-negative.")
        if p < 0:
            p = 0.0
        idx = int(bitstr, 2)
        probs[idx] += p
        total += p

    if total <= 0:
        raise ValueError("Sum of probabilities must be positive.")

    probs /= total
    amps = np.sqrt(probs).astype(complex)

    qc = QuantumCircuit(n, n)
    qc.initialize(Statevector(amps), range(n))
    qc.measure(range(n), range(n))
    return qc
