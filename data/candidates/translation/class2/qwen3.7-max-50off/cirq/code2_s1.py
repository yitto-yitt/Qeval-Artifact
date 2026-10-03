# EVAL_META: task_id=2, framework=cirq, class=2
import numpy as np
from math import sqrt

def create_bell_statevector():
    return np.array([1, 0, 0, 1], dtype=np.complex128) / sqrt(2)
