# EVAL_META: task_id=13, framework=qiskit, class=3
from qiskit import QuantumCircuit
import numpy as np


def custom_rotation_gate():
    qc = QuantumCircuit(1)
    qc.u(np.pi / 2, np.pi / 2, np.pi / 2, 0)
    return qc
