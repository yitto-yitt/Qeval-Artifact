# EVAL_META: task_id=41, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import *

def compose_op():
    I = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)

    op = np.eye(2**3, dtype=complex)

    # Embed Pauli "YX" on qargs=[0,2] for 3 qubits (q0 as most-significant in kron order q0⊗q1⊗q2)
    yx_embedded = np.kron(np.kron(Y, I), X)

    # Qiskit compose(..., front=True): self @ other
    return op @ yx_embedded
