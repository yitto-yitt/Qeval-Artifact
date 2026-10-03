# EVAL_META: task_id=120, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import Diagonal
import math


def create_diagonal_circuit(diag):
    num_qubits = int(math.log2(len(diag)))
    if 2**num_qubits != len(diag):
        raise ValueError("Length of diag must be a power of 2.")
    qc = QuantumCircuit(num_qubits)
    qc.append(Diagonal(diag), range(num_qubits))
    return qc
