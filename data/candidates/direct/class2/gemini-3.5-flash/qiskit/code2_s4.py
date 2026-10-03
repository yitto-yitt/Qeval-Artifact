# EVAL_META: task_id=2, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import Statevector

def create_bell_statevector():
    return Statevector([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)])
