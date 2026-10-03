# EVAL_META: task_id=117, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, QGate, matrix_decompose


def decompose_unitary(unitary):
    if hasattr(unitary, "data"):
        u = np.array(unitary.data, dtype=complex)
    elif hasattr(unitary, "to_matrix"):
        u = np.array(unitary.to_matrix(), dtype=complex)
    else:
        u = np.array(unitary, dtype=complex)

    circuit = matrix_decompose([0, 1], u)
    return circuit
