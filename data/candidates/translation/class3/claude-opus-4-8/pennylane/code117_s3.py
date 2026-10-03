# EVAL_META: task_id=117, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def decompose_unitary(unitary):
    U = np.asarray(unitary)
    return qml.ops.two_qubit_decomposition(U, wires=[0, 1])
