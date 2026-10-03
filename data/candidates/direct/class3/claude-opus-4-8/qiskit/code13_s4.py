# EVAL_META: task_id=13, framework=qiskit, class=3
from qiskit import QuantumCircuit
from math import pi


def custom_rotation_gate():
    qc = QuantumCircuit(1)
    qc.u(pi / 2, pi / 2, pi / 2, 0)
    return qc
