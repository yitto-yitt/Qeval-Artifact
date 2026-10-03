# EVAL_META: task_id=13, framework=qiskit, class=3

import numpy as np
from qiskit import QuantumCircuit

def custom_rotation_gate():
    qc = QuantumCircuit(1)
    qc.u(np.pi/2, np.pi/2, np.pi/2, 0)
    return qc
