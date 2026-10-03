# EVAL_META: task_id=41, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)


def compose_op():
    # 3-qubit identity: 8x8 identity matrix
    identity_3q = np.eye(2**3, dtype=complex)

    # YX Pauli: Y⊗X = kron(Y, X)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    yx = np.kron(Y, X)  # 4x4 matrix acting on 2 qubits

    # compose(yx, qargs=[0,2], front=True) means:
    # result = op @ embed(yx, qargs=[0,2])
    # embed yx into the 3-qubit space on qubits 0 and 2
    # qubit ordering: Qiskit uses little-endian (qubit 0 = least significant)
    # For a 3-qubit system with qargs=[0,2], qubit 1 is the "middle" index
    # We need to embed the 4x4 yx operator acting on qubits 0 and 2
    # into the full 8x8 space, leaving qubit 1 free (tensored with I)

    # Qiskit qubit ordering: qubit 0 is rightmost (LSB)
    # state ordering: |q2 q1 q0> -> index = q2*4 + q1*2 + q0
    # yx acts on qargs=[0,2]: q0 gets X (right factor), q2 gets Y (left factor)
    # So in full space: embed as Y_{q2} ⊗ I_{q1} ⊗ X_{q0}
    I = np.eye(2, dtype=complex)
    # kron in Qiskit big-endian layout: leftmost = highest qubit index
    # full = Y ⊗ I ⊗ X  (q2, q1, q0)
    full_yx = np.kron(np.kron(Y, I), X)  # 8x8

    # compose with front=True: result = embed_yx @ identity = embed_yx
    result = identity_3q @ full_yx

    return result


machine.finalize()
