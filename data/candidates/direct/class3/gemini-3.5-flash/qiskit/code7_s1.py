# EVAL_META: task_id=7, framework=qiskit, class=3

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

def create_parametrized_gate():
    theta = Parameter('theta')
    qc = QuantumCircuit(1)
    qc.rx(theta, 0)
    return qc
