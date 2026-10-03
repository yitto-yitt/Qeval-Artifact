# EVAL_META: task_id=77, framework=qiskit, class=1
import math
from qiskit import QuantumCircuit


def circuit_from_probability_dist(probability_dist):
    if not probability_dist:
        return QuantumCircuit(1, 1)

    keys = list(probability_dist.keys())

    if all(isinstance(k, int) for k in keys):
        n = max(1, max(k.bit_length() for k in keys))
        size = 1 << n
        amplitudes = [0.0] * size
        total = sum(float(p) for p in probability_dist.values())
        if total <= 0:
            amplitudes[0] = 1.0
        else:
            for k, p in probability_dist.items():
                if 0 <= k < size and p > 0:
                    amplitudes[k] = math.sqrt(float(p) / total)
    else:
        str_keys = [str(k).replace(" ", "") for k in keys]
        n = max(1, max(len(k) for k in str_keys))
        size = 1 << n
        amplitudes = [0.0] * size
        total = sum(float(p) for p in probability_dist.values())
        if total <= 0:
            amplitudes[0] = 1.0
        else:
            for original_key, p in probability_dist.items():
                key = str(original_key).replace(" ", "")
                if not key:
                    idx = 0
                else:
                    idx = int(key.zfill(n), 2)
                if 0 <= idx < size and p > 0:
                    amplitudes[idx] = math.sqrt(float(p) / total)

    qc = QuantumCircuit(n, n)
    qc.initialize(amplitudes, list(range(n)))
    qc.measure(list(range(n)), list(range(n)))
    return qc
