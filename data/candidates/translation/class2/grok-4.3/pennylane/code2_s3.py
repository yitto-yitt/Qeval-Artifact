# EVAL_META: task_id=2, framework=pennylane, class=2
from math import sqrt
import pennylane as qml


def create_bell_statevector():
    state_00 = qml.numpy.array([1, 0, 0, 0])
    state_11 = qml.numpy.array([0, 0, 0, 1])
    return (state_00 + state_11) / sqrt(2)
