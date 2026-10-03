# EVAL_META: task_id=66, framework=qiskit, class=2
from math import acos, pi, sqrt
from qiskit import QuantumCircuit


def w_state():
    qc = QuantumCircuit(3, 3)
    qc.x(0)
    qc.cry(2 * acos(1 / sqrt(3)), 0, 1)
    qc.cx(1, 0)
    qc.cry(pi / 2, 1, 2)
    qc.cx(2, 1)
    qc.measure(range(3), range(3))
    return qc
