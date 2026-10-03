# EVAL_META: task_id=13, framework=qiskit, class=3
from qiskit import QuantumCircuit
import numpy as np

def custom_rotation_gate():
    qc = QuantumCircuit(1)
    theta = np.pi / 2
    phi = np.pi / 2
    lam = np.pi / 2
    qc.u(theta, phi, lam, 0)
    return qc
