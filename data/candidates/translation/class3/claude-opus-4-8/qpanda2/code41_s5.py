# EVAL_META: task_id=41, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)


def compose_op():
    # 3-qubit identity: 8x8 identity matrix
    identity_3q = np.eye(2**3, dtype=complex)

    # YX as 4x4 matrix: Y⊗X (tensor product, big-endian: first Pauli is most significant)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    # Pauli("YX") in Qiskit is qubit-order little-endian: rightmost is qubit 0
    # YX means qubit 0 gets X, qubit 1 gets Y => matrix = Y ⊗ X (standard tensor)
    yx_matrix = np.kron(Y, X)

    # compose(yx, qargs=[0,2], front=True):
    # front=True means yx acts before the identity, so result = identity @ (yx ⊗ I_q1)
    # Embed yx_matrix acting on qubits [0,2] of a 3-qubit space
    # Qiskit qubit ordering: qubit 0 is least significant bit
    # Construct the full 8x8 matrix for yx on qubits 0 and 2, identity on qubit 1
    full_matrix = np.zeros((8, 8), dtype=complex)
    for i in range(8):
        for j in range(8):
            # Extract qubit indices: bit0=qubit0, bit1=qubit1, bit2=qubit2
            i0 = (i >> 0) & 1
            i1 = (i >> 1) & 1
            i2 = (i >> 2) & 1
            j0 = (j >> 0) & 1
            j1 = (j >> 1) & 1
            j2 = (j >> 2) & 1
            # qubit 1 must be unchanged
            if i1 != j1:
                continue
            # yx acts on (qubit2, qubit0): row index in yx = i2*2+i0, col = j2*2+j0
            yx_row = i2 * 2 + i0
            yx_col = j2 * 2 + j0
            full_matrix[i, j] = yx_matrix[yx_row, yx_col]

    # identity_3q @ full_matrix = full_matrix (front=True: yx first, then identity)
    result_matrix = identity_3q @ full_matrix
    return result_matrix


machine.finalize()
