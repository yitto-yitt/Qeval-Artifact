# EVAL_META: task_id=77, framework=cirq, class=1
import math
import numpy as np
import cirq

def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = []
    for basis_state in range(2**num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))

    v = np.array(amplitudes, dtype=float)
    norm = np.linalg.norm(v)
    if norm > 0:
        v = v / norm

    e0 = np.zeros_like(v)
    e0[0] = 1.0
    w = v - e0
    w_norm_sq = np.dot(w, w)
    if w_norm_sq > 1e-12:
        U = np.eye(len(v), dtype=complex) - 2 * np.outer(w, w) / w_norm_sq
    else:
        U = np.eye(len(v), dtype=complex)

    qubits = cirq.LineQubit.range(num_qubits)
    gate = cirq.MatrixGate(U)
    circuit = cirq.Circuit(gate.on(*qubits[::-1]))
    return circuit
