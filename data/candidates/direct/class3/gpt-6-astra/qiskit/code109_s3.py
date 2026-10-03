# EVAL_META: task_id=109, framework=qiskit, class=3
from math import pi
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter


def circuit():
    theta = Parameter("theta")
    qc = QuantumCircuit(1)
    qc.u(pi / 2, theta, 0, 0)
    return qc
