# EVAL_META: task_id=2, framework=pennylane, class=2
from math import sqrt

import numpy as np


def create_bell_statevector():
    return np.array([1, 0, 0, 1], dtype=complex) / sqrt(2)
