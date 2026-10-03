# EVAL_META: task_id=58, framework=qiskit, class=3

import numpy as np
from qiskit import QuantumCircuit

def create_ch_gate():
    qc = QuantumCircuit(2)
    qc.ry(np.pi / 4, 1)
    qc.cx(0, 1)
    qc.ry(-np.pi / 4, 1)
    return qc
