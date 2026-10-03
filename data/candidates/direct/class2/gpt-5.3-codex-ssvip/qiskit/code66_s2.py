# EVAL_META: task_id=66, framework=qiskit, class=2
from qiskit import QuantumCircuit


def w_state():
    qc = QuantumCircuit(3, 3)
    theta = 2 * __import__("math").asin(1 / __import__("math").sqrt(3))
    qc.ry(theta, 0)
    qc.ch(0, 1)
    qc.x(0)
    qc.cx(1, 2)
    qc.cx(0, 1)
    qc.measure([0, 1, 2], [0, 1, 2])
    return qc
