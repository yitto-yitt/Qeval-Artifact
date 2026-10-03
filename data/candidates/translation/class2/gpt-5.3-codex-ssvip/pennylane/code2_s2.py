# EVAL_META: task_id=2, framework=pennylane, class=2
import pennylane as qml
import numpy as np


def create_bell_statevector():
    return qml.math.asarray([1 / np.sqrt(2), 0, 0, 1 / np.sqrt(2)], like="numpy")
