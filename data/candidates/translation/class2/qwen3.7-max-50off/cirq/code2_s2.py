# EVAL_META: task_id=2, framework=cirq, class=2
import numpy as np

def create_bell_statevector():
    return np.array([1 / np.sqrt(2), 0, 0, 1 / np.sqrt(2)], dtype=np.complex128)
