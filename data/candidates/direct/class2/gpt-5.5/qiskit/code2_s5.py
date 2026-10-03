# EVAL_META: task_id=2, framework=qiskit, class=2
from qiskit.quantum_info import Statevector
import numpy as np


def create_bell_statevector():
    return Statevector([1 / np.sqrt(2), 0, 0, 1 / np.sqrt(2)])
