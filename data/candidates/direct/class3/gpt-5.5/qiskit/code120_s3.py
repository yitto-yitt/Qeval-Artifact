# EVAL_META: task_id=120, framework=qiskit, class=3
from qiskit import QuantumCircuit

try:
    from qiskit.circuit.library import DiagonalGate as Diagonal
except ImportError:
    from qiskit.circuit.library import Diagonal


def create_diagonal_circuit(diag):
    num_qubits = (len(diag) - 1).bit_length()
    circuit = QuantumCircuit(num_qubits)
    circuit.append(Diagonal(diag), range(num_qubits))
    return circuit
