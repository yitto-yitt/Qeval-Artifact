# EVAL_META: task_id=2, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import Statevector

def create_bell_statevector():
    return Statevector(np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2))
