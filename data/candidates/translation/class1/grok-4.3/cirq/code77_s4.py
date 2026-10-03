# EVAL_META: task_id=77, framework=cirq, class=1
import math
import numpy as np
import cirq

def gram_schmidt(vectors):
    basis = []
    for v in vectors:
        w = v.copy()
        for b in basis:
            w -= np.dot(b.conj(), w) * b
        norm = np.linalg.norm(w)
        if norm > 1e-10:
            basis.append(w / norm)
    return basis

def circuit_from_probability_dist(probability_dist):
    if not probability_dist:
        num_qubits = 1
    else:
        max_state = max(probability_dist.keys())
        num_qubits = math.ceil(math.log2(max_state + 1)) or 1
    dim = 2 ** num_qubits
    amplitudes = np.zeros(dim, dtype=complex)
    for basis_state, prob in probability_dist.items():
        amplitudes[basis_state] = math.sqrt(prob)
    norm = np.linalg.norm(amplitudes)
    if norm > 0:
        amplitudes /= norm
    mat = np.zeros((dim, dim), dtype=complex)
    mat[:, 0] = amplitudes
    other_vectors = [np.eye(dim, dtype=complex)[:, i] for i in range(1, dim)]
    vectors = [amplitudes] + other_vectors
    ortho_basis = gram_schmidt(vectors)
    for i, vec in enumerate(ortho_basis):
        mat[:, i] = vec
    qubits = cirq.LineQubit.range(num_qubits)
    gate = cirq.MatrixGate(mat)
    circuit = cirq.Circuit(gate.on(*qubits))
    return circuit
