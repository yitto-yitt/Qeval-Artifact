# EVAL_META: task_id=77, framework=cirq, class=1
import math

import cirq
import numpy as np


def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = []
    for basis_state in range(2**num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))

    state = np.array(amplitudes, dtype=np.complex128)
    dim = 2**num_qubits
    e0 = np.zeros(dim, dtype=np.complex128)
    e0[0] = 1.0

    diff = e0 - state
    diff_norm = np.linalg.norm(diff)
    if diff_norm == 0.0:
        unitary = np.eye(dim, dtype=np.complex128)
    else:
        u = diff / diff_norm
        unitary = np.eye(dim, dtype=np.complex128) - 2 * np.outer(u, np.conjugate(u))

    qubits = cirq.LineQubit.range(num_qubits)
    return cirq.Circuit(cirq.MatrixGate(unitary).on(*qubits))
