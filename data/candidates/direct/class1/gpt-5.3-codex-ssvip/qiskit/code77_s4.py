# EVAL_META: task_id=77, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import math


def circuit_from_probability_dist(probability_dist):
    if not isinstance(probability_dist, dict) or len(probability_dist) == 0:
        raise ValueError("probability_dist must be a non-empty dictionary.")

    keys = list(probability_dist.keys())
    if not all(isinstance(k, str) and len(k) > 0 and set(k).issubset({"0", "1"}) for k in keys):
        raise ValueError("All keys must be non-empty bitstrings containing only '0' and '1'.")

    n = len(keys[0])
    if any(len(k) != n for k in keys):
        raise ValueError("All bitstrings must have the same length.")

    probs = {}
    for k, v in probability_dist.items():
        if v is None or v < 0:
            raise ValueError("Probabilities must be non-negative.")
        probs[k] = float(v)

    total = sum(probs.values())
    if total <= 0:
        raise ValueError("Sum of probabilities must be positive.")

    norm_probs = {k: v / total for k, v in probs.items()}

    dim = 2 ** n
    amplitudes = [0.0] * dim
    for bitstr, p in norm_probs.items():
        idx = int(bitstr, 2)
        amplitudes[idx] = math.sqrt(p)

    sv = Statevector(amplitudes)
    qc = QuantumCircuit(n, n)
    qc.initialize(sv.data, list(range(n)))
    qc.measure(range(n), range(n))
    return qc
