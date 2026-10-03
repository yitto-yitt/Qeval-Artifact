# EVAL_META: task_id=66, framework=qiskit, class=2
from math import asin, sqrt
from qiskit import QuantumCircuit


def w_state():
    qc = QuantumCircuit(3, 3)
    qc.ry(2 * asin(1 / sqrt(3)), 0)
    qc.x(0)
    qc.ch(0, 1)
    qc.cx(1, 2)
    qc.cx(0, 2)
    qc.x(0)
    qc.measure([0, 1, 2], [0, 1, 2])
    return qc
