# EVAL_META: task_id=7, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter


def create_parametrized_gate():
    circuit = QuantumCircuit(1)
    theta = Parameter("theta")
    circuit.rx(theta, 0)
    return circuit
