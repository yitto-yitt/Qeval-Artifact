# EVAL_META: task_id=117, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def decompose_unitary(unitary):
    U = np.asarray(unitary, dtype=complex)
    return qml.transforms.two_qubit_decomposition(U, wires=[0, 1])
