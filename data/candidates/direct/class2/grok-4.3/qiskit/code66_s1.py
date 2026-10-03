# EVAL_META: task_id=66, framework=qiskit, class=2
import numpy as np
from qiskit import QuantumCircuit

def w_state():
    qc = QuantumCircuit(3, 3)
    w_state_vec = np.array([0, 1, 1, 0, 1, 0, 0, 0]) / np.sqrt(3)
    qc.initialize(w_state_vec, [0, 1, 2])
    qc.measure([0, 1, 2], [0, 1, 2])
    return qc
