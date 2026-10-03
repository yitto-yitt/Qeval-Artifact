# EVAL_META: task_id=66, framework=qiskit, class=2
from qiskit import QuantumCircuit
import numpy as np

def w_state():
    qc = QuantumCircuit(3, 3)
    w = np.array([0, 1/np.sqrt(3), 1/np.sqrt(3), 0, 1/np.sqrt(3), 0, 0, 0])
    qc.initialize(w, [0, 1, 2])
    qc.measure([0, 1, 2], [0, 1, 2])
    return qc
