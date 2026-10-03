# EVAL_META: task_id=2, framework=cirq, class=2
from math import sqrt
import numpy as np
import cirq


def create_bell_statevector():
    return cirq.StateVector(np.array([1 / sqrt(2), 0, 0, 1 / sqrt(2)], dtype=complex))
