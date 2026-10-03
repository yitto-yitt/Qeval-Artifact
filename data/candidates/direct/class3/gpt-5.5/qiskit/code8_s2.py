# EVAL_META: task_id=8, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter


def rx_gate(value):
    theta = Parameter("theta")
    circuit = QuantumCircuit(1)
    circuit.rx(theta, 0)
    if value is not None:
        circuit = circuit.assign_parameters({theta: value}, inplace=False)
    return circuit
