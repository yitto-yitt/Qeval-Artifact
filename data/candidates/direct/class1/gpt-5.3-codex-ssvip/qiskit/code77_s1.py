# EVAL_META: task_id=77, framework=qiskit, class=1
from math import log2
from qiskit import QuantumCircuit


def circuit_from_probability_dist(probability_dist):
    if not isinstance(probability_dist, dict) or len(probability_dist) == 0:
        raise ValueError("probability_dist must be a non-empty dictionary.")

    keys = list(probability_dist.keys())
    if not all(isinstance(k, str) for k in keys):
        raise ValueError("All keys in probability_dist must be bitstring strings.")

    n = len(keys[0])
    if n == 0 or any(len(k) != n for k in keys):
        raise ValueError("All bitstrings must have the same non-zero length.")
    if any(ch not in "01" for k in keys for ch in k):
        raise ValueError("Bitstrings must contain only '0' and '1'.")

    dim = 2 ** n
    probs = [0.0] * dim
    total = 0.0

    for bitstr, p in probability_dist.items():
        if p is None:
            raise ValueError("Probabilities must be numeric.")
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
    probs = [p / total for p in probs]

    amps = [p ** 0.5 for p in probs]

    qc = QuantumCircuit(n, n)
    qc.initialize(amps, list(range(n)))
    qc.measure(range(n), range(n))
    return qc
