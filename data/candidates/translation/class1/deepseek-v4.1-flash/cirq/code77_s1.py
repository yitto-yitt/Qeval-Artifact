# EVAL_META: task_id=77, framework=cirq, class=1
import math
import numpy as np
import cirq


def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    dim = 2 ** num_qubits
    amplitudes = np.zeros(dim, dtype=float)
    for basis_state in range(dim):
        prob = probability_dist.get(basis_state, 0)
        amplitudes[basis_state] = math.sqrt(prob)

    norm = np.linalg.norm(amplitudes)
    if norm > 1e-12:
        amplitudes = amplitudes / norm

    e0 = np.zeros(dim, dtype=float)
    e0[0] = 1.0
    u = e0 - amplitudes
    norm_u_sq = np.dot(u, u)
    if norm_u_sq > 1e-12:
        U = np.eye(dim) - 2.0 * np.outer(u, u) / norm_u_sq
    else:
        U = np.eye(dim)

    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit(cirq.MatrixGate(U).on(*qubits))
    return circuit
