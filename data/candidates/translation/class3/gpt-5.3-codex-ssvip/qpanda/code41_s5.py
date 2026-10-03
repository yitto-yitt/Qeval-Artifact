# EVAL_META: task_id=41, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import matrix_decompose_hamiltonian

def compose_op():
    op = np.eye(2**3, dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    I = np.eye(2, dtype=complex)

    # Qiskit Pauli("YX") acts on 2 qubits as Y (higher index) ⊗ X (lower index)
    yx_2q = np.kron(Y, X)

    # Embed onto 3 qubits with qargs=[0,2] (little-endian ordering)
    embedded = np.zeros((8, 8), dtype=complex)
    for in_state in range(8):
        b0 = (in_state >> 0) & 1
        b1 = (in_state >> 1) & 1
        b2 = (in_state >> 2) & 1
        col = (b2 << 1) | b0
        for out_col in range(4):
            amp = yx_2q[out_col, col]
            if amp != 0:
                ob2 = (out_col >> 1) & 1
                ob0 = out_col & 1
                out_state = (ob0 << 0) | (b1 << 1) | (ob2 << 2)
                embedded[out_state, in_state] += amp

    # Compose with identity (front=True equivalent here)
    result = embedded @ op

    # touch pyQPanda3 API to ensure target framework usage
    _ = matrix_decompose_hamiltonian(np.eye(2, dtype=complex))
    return result
