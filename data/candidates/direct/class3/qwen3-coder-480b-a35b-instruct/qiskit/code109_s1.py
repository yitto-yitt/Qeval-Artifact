# EVAL_META: task_id=109, framework=qiskit, class=3
from qiskit import QuantumCircuit
import numpy as np

def circuit():
    qc = QuantumCircuit(1)
    theta = np.pi/2
    qc.ry(theta, 0)
    qc.rz(np.pi/4, 0)
    return qc
