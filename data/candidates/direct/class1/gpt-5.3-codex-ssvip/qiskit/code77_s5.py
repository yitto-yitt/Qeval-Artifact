# EVAL_META: task_id=77, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import math


def circuit_from_probability_dist(probability_dist):
    if not isinstance(probability_dist, dict) or len(probability_dist) == 0:
        raise ValueError("probability_dist must be a non-empty dictionary.")

    keys = list(probability_dist.keys())
    if not all(isinstance(k, str) for k in keys):
        raise ValueError("All measurement keys must be bitstrings.")

    n = len(keys[0])
    if n == 0 or any(len(k) != n for k in keys):
        raise ValueError("All bitstrings must have the same non-zero length.")

    probs = {}
    total = 0.0
    for k, v in probability_dist.items():
        if any(ch not in "01" for ch in k):
            raise ValueError("Measurement keys must be bitstrings containing only '0' and '1'.")
        p = float(v)
        if p < -1e-15:
            raise ValueError("Probabilities must be non-negative.")
        if p < 0:
            p = 0.0
        probs[k] = p
        total += p

    if total <= 0:
        raise ValueError("Sum of probabilities must be positive.")

    # Normalize probabilities
    for k in probs:
        probs[k] /= total

    dim = 1 << n
    amplitudes = [0.0] * dim

    # Qiskit basis index uses little-endian bit ordering.
    # Measurement strings are interpreted in standard order q_{n-1}...q_0.
    for bitstr, p in probs.items():
        idx = int(bitstr[::-1], 2)
        amplitudes[idx] = math.sqrt(p)

    # Validate normalization tolerance
    norm = sum(a * a for a in amplitudes)
    if not math.isclose(norm, 1.0, rel_tol=1e-9, abs_tol=1e-9):
        scale = math.sqrt(norm)
        amplitudes = [a / scale for a in amplitudes]

    qc = QuantumCircuit(n, n)
    qc.initialize(amplitudes, list(range(n)))
    qc.measure(range(n), range(n))
    return qc
