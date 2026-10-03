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
    qubits = cirq.LineQubit.range(num_qubits)
    vec = np.array(amplitudes, dtype=complex)
    dim = len(vec)
    mat = np.eye(dim, dtype=complex)
    mat[:, 0] = vec
    for i in range(1, dim):
        for j in range(i):
            mat[:, i] -= np.dot(mat[:, j].conj(), mat[:, i]) * mat[:, j]
        norm = np.linalg.norm(mat[:, i])
        if norm > 1e-10:
            mat[:, i] /= norm
    gate = cirq.MatrixGate(mat)
    circuit = cirq.Circuit(gate.on(*qubits))
    return circuit
