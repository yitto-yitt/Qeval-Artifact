# EVAL_META: task_id=66, framework=qiskit, class=2
import numpy as np
from qiskit import QuantumCircuit

def w_state():
    qc = QuantumCircuit(3, 3)

    theta = 2 * np.arcsin(1 / np.sqrt(3))
    qc.ry(theta, 0)

    bell = QuantumCircuit(2)
    bell.h(0)
    bell.cx(0, 1)
    bell.x(1)

    controlled_bell = bell.to_gate().control(1, ctrl_state=0)
    qc.append(controlled_bell, [0, 1, 2])

    qc.measure([0, 1, 2], [0, 1, 2])
    return qc
