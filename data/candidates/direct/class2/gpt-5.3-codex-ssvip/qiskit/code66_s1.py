# EVAL_META: task_id=66, framework=qiskit, class=2
from qiskit import QuantumCircuit
import math

def w_state():
    qc = QuantumCircuit(3, 3)
    theta1 = 2 * math.asin(1 / math.sqrt(3))
    theta2 = math.pi / 2
    qc.ry(theta1, 0)
    qc.ch(0, 1)
    qc.x(0)
    qc.cx(1, 2)
    qc.cx(0, 1)
    qc.ry(theta2, 0)
    qc.x(0)
    qc.measure([0, 1, 2], [0, 1, 2])
    return qc
