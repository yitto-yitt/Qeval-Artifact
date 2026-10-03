# EVAL_META: task_id=66, framework=qiskit, class=2

import numpy as np
from qiskit import QuantumCircuit

def w_state():
    qc = QuantumCircuit(3, 3)
    
    # Angle for the first rotation
    theta = 2 * np.arccos(1 / np.sqrt(3))
    qc.ry(theta, 0)
    
    # Controlled-Hadamard
    qc.ch(0, 1)
    
    # CNOT gates to distribute the state
    qc.cx(1, 2)
    qc.cx(0, 1)
    qc.x(0)
    
    # Measure the qubits
    qc.measure([0, 1, 2], [0, 1, 2])
    
    return qc
