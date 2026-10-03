# EVAL_META: task_id=77, framework=qiskit, class=1

import numpy as np
from qiskit import QuantumCircuit


def circuit_from_probability_dist(probability_dist):
    if not probability_dist:
        return QuantumCircuit()

    items = list(probability_dist.items())

    if all(isinstance(key, int) for key, _ in items):
        n = max(1, max((int(key).bit_length() for key, _ in items), default=1))
        key_strings = {format(int(key), f"0{n}b"): prob for key, prob in items}
    else:
        keys = [str(key) for key, _ in items]
        n = max(len(key) for key in keys)
        if n == 0:
            n = 1
        key_strings = {str(key).zfill(n): prob for key, prob in items}

    dim = 2 ** n
    amplitudes = np.zeros(dim, dtype=complex)

    for bitstring, prob in key_strings.items():
        idx = int(bitstring, 2)
        amplitudes[idx] = np.sqrt(prob)

    norm = np.linalg.norm(amplitudes)
    if norm > 0:
        amplitudes = amplitudes / norm

    qc = QuantumCircuit(n)
    qc.prepare_state(amplitudes, qc.qubits)
    return qc
