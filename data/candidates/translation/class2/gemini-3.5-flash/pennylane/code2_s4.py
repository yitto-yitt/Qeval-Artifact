# EVAL_META: task_id=2, framework=pennylane, class=2
import pennylane as qml
from pennylane import numpy as np

def create_bell_statevector():
    return np.array([1.0, 0.0, 0.0, 1.0]) / np.sqrt(2)
