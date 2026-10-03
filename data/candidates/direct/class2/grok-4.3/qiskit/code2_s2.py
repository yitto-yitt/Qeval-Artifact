# EVAL_META: task_id=2, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import Statevector

def create_bell_statevector():
    return (Statevector.from_label("00") + Statevector.from_label("11")) / np.sqrt(2)
