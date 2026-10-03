# EVAL_META: task_id=5, framework=qiskit, class=2
from qiskit import QuantumCircuit


def create_state_prep():
    circuit = QuantumCircuit(2)
    circuit.x(0)
    return circuit
