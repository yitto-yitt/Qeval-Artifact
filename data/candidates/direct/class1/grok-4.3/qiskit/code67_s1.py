# EVAL_META: task_id=67, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit

def chsh_circuit(alice, bob):
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.ry(-alice * np.pi / 2, 0)
    qc.ry((2 * bob - 1) * np.pi / 4, 1)
    qc.measure([0, 1], [0, 1])
    return qc
