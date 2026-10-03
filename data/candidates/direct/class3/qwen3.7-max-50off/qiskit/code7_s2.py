# EVAL_META: task_id=7, framework=qiskit, class=3
from qiskit.circuit import QuantumCircuit, Parameter

def create_parametrized_gate():
    qc = QuantumCircuit(1)
    theta = Parameter('theta')
    qc.rx(theta, 0)
    return qc
