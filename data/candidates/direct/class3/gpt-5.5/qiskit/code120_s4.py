# EVAL_META: task_id=120, framework=qiskit, class=3
import math
from qiskit import QuantumCircuit
from qiskit.circuit.library import DiagonalGate


def create_diagonal_circuit(diag):
    num_qubits = int(math.log2(len(diag)))
    circuit = QuantumCircuit(num_qubits)
    circuit.append(DiagonalGate(diag), range(num_qubits))
    return circuit
