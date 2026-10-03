# EVAL_META: task_id=66, framework=qiskit, class=2
import numpy as np
from qiskit import QuantumCircuit

def w_state():
    qc = QuantumCircuit(3, 3)
    theta = 2 * np.arcsin(1 / np.sqrt(3))
    qc.ry(theta, 0)
    qc.x(0)
    qc.cry(np.pi / 2, 0, 1)
    qc.x(1)
    qc.ccx(0, 1, 2)
    qc.x(1)
    qc.x(0)
    qc.measure(qc.qubits, qc.clbits)
    return qc
