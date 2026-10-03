# EVAL_META: task_id=109, framework=qiskit, class=3
from math import pi
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

def circuit():
    phi = Parameter("phi")
    qc = QuantumCircuit(1)
    qc.u(pi / 2, phi, 0)
    return qc
