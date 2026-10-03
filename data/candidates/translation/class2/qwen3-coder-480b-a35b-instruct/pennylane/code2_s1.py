# EVAL_META: task_id=2, framework=pennylane, class=2
import pennylane as qml
from numpy import array, sqrt


def create_bell_statevector():
    return array([1, 0, 0, 1]) / sqrt(2)
