# EVAL_META: task_id=66, framework=qiskit, class=2
import math
from qiskit import QuantumCircuit


def w_state():
    qc = QuantumCircuit(3, 3)
    theta = 2 * math.acos(1 / math.sqrt(3))
    qc.ry(theta, 2)
    qc.ch(2, 1)
    qc.cx(1, 0)
    qc.cx(2, 0)
    qc.x(2)
    qc.measure([0, 1, 2], [0, 1, 2])
    return qc
