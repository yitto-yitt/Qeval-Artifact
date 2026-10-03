# EVAL_META: task_id=120, framework=qiskit, class=3
from math import log2
from qiskit import QuantumCircuit
from qiskit.circuit.library import DiagonalGate


def create_diagonal_circuit(diag):
    num_qubits = int(log2(len(diag)))
    circuit = QuantumCircuit(num_qubits)
    circuit.append(DiagonalGate(diag), range(num_qubits))
    return circuit
