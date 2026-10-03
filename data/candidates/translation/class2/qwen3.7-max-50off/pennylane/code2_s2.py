# EVAL_META: task_id=2, framework=pennylane, class=2
import numpy as np
from math import sqrt

def create_bell_statevector():
    return np.array([1 / sqrt(2), 0, 0, 1 / sqrt(2)], dtype=complex)
