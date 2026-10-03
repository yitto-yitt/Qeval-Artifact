# EVAL_META: task_id=8, framework=qiskit, class=3
from qiskit.circuit import QuantumCircuit, Parameter

def rx_gate(value):
    qc = QuantumCircuit(1)
    theta = Parameter('theta')
    qc.rx(theta, 0)
    if value is not None:
        qc = qc.assign_parameters({theta: value})
    return qc
