# EVAL_META: task_id=120, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import DiagonalGate


def create_diagonal_circuit(diag):
    gate = DiagonalGate(diag)
    circuit = QuantumCircuit(gate.num_qubits)
    circuit.append(gate, range(gate.num_qubits))
    return circuit
