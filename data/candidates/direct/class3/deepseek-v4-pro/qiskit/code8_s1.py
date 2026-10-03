# EVAL_META: task_id=8, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

def rx_gate(value):
    theta = Parameter('theta')
    qc = QuantumCircuit(1)
    qc.rx(theta, 0)
    if value is not None:
        qc = qc.assign_parameters({theta: value})
    return qc
