# EVAL_META: task_id=2, framework=qiskit, class=2

import numpy as np
from qiskit.quantum_info import Statevector

def create_bell_statevector():
    """
    Returns a Phi+ Bell statevector: (|00> + |11>) / sqrt(2)
    """
    return Statevector([1 / np.sqrt(2), 0, 0, 1 / np.sqrt(2)])
