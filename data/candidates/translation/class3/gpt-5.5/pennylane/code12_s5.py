# EVAL_META: task_id=12, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def get_unitary():
    h = qml.matrix(qml.Hadamard(wires=0), wire_order=[1, 0])
    cx = qml.matrix(qml.CNOT(wires=[0, 1]), wire_order=[1, 0])
    return np.asarray(cx @ h, dtype=complex)
