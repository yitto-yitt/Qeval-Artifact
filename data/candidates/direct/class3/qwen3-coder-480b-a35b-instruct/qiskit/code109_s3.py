# EVAL_META: task_id=109, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter


def circuit():
    theta = Parameter('theta')
    qc = QuantumCircuit(1)
    qc.ry(theta, 0)
    return qc
