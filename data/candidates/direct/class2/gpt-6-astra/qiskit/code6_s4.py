# EVAL_META: task_id=6, framework=qiskit, class=2
from qiskit import QuantumCircuit


def create_state_prep(num_qubits):
    circuit = QuantumCircuit(num_qubits)
    circuit.x(0)
    return circuit
