# EVAL_META: task_id=8, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

def rx_gate(value):
    qc = QuantumCircuit(1)
    theta = Parameter('theta')
    qc.rx(theta, 0)
    if value is not None:
        qc.assign_parameters({theta: value}, inplace=True)
    return qc
