# EVAL_META: task_id=66, framework=qiskit, class=2

import numpy as np
from qiskit import QuantumCircuit

def w_state():
    qc = QuantumCircuit(3)
    
    theta1 = 2 * np.arccos(1 / np.sqrt(3))
    theta2 = 2 * np.arccos(1 / np.sqrt(2))
    
    qc.x(0)
    qc.cry(theta1, 0, 1)
    qc.cx(1, 0)
    qc.cry(theta2, 1, 2)
    qc.cx(2, 1)
    
    qc.measure_all()
    return qc
