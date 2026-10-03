# EVAL_META: task_id=109, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from math import pi

def circuit():
    phi = Parameter("phi")
    qc = QuantumCircuit(1)
    qc.u(pi / 2, phi, 0, 0)
    return qc
