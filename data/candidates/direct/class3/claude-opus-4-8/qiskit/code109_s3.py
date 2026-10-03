# EVAL_META: task_id=109, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter


def circuit():
    phi = Parameter("phi")
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.p(phi, 0)
    return qc
