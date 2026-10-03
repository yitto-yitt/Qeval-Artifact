# EVAL_META: task_id=2, framework=pennylane, class=2
from math import sqrt
import pennylane as qml


def create_bell_statevector():
    return qml.numpy.array([1 / sqrt(2), 0, 0, 1 / sqrt(2)])
