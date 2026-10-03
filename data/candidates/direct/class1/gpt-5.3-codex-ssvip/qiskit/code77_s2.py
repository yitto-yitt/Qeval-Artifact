# EVAL_META: task_id=77, framework=qiskit, class=1
import math
from qiskit import QuantumCircuit


def circuit_from_probability_dist(probability_dist):
    if not probability_dist:
        qc = QuantumCircuit(1, 1)
        qc.measure(0, 0)
        return qc

    keys = list(probability_dist.keys())
    max_len = max(len(k) for k in keys) if keys else 1
    n = max(1, max_len)

    dim = 1 << n
    amplitudes = [0.0] * dim

    total_prob = 0.0
    for bitstr, prob in probability_dist.items():
        p = float(prob)
        if p < 0:
            p = 0.0
        total_prob += p

    if total_prob <= 0:
        amplitudes[0] = 1.0
    else:
        for bitstr, prob in probability_dist.items():
            p = float(prob)
            if p <= 0:
                continue
            b = bitstr.zfill(n)
            idx = int(b, 2)
            amplitudes[idx] = math.sqrt(p / total_prob)

    qc = QuantumCircuit(n, n)
    qc.initialize(amplitudes, list(range(n)))
    qc.measure(range(n), range(n))
    return qc
