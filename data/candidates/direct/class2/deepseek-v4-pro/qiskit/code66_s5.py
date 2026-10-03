# EVAL_META: task_id=66, framework=qiskit, class=2
import numpy as np
from qiskit import QuantumCircuit

def w_state():
    qc = QuantumCircuit(3, 3)
    theta = 2 * np.arccos(np.sqrt(2 / 3))
    qc.ry(theta, 0)
    qc.ch(0, 1, ctrl_state=0)
    qc.x([0, 1])
    qc.ccx(0, 1, 2)
    qc.x([0, 1])
    qc.measure([0, 1, 2], [0, 1, 2])
    return qc
