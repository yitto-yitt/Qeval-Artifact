# EVAL_META: task_id=109, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

def circuit():
    qc = QuantumCircuit(1)
    qc.h(0)
    theta = Parameter('θ')
    qc.rz(theta, 0)
    return qc
