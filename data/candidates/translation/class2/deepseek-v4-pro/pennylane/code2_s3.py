# EVAL_META: task_id=2, framework=pennylane, class=2
from math import sqrt

import numpy as np


def create_bell_statevector():
    state_00 = np.zeros(4, dtype=complex)
    state_11 = np.zeros(4, dtype=complex)
    state_00[0] = 1
    state_11[3] = 1
    return (state_00 + state_11) / sqrt(2)
