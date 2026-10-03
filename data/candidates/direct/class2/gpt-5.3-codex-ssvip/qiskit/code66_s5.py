# EVAL_META: task_id=66, framework=qiskit, class=2
from qiskit import QuantumCircuit


def w_state():
    qc = QuantumCircuit(3, 3)
    theta = 2.0 * (2.0 ** 0.5) / 3.0
    qc.ry(theta, 0)
    qc.ch(0, 1)
    qc.cx(1, 2)
    qc.cx(0, 1)
    qc.x(0)
    qc.measure([0, 1, 2], [0, 1, 2])
    return qc
