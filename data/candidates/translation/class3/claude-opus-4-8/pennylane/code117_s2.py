# EVAL_META: task_id=117, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def decompose_unitary(unitary):
    U = np.asarray(unitary, dtype=complex)
    return qml.ops.two_qubit_decomposition(U, wires=[0, 1])
