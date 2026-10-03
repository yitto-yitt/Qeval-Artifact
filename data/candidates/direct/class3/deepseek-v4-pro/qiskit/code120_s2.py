# EVAL_META: task_id=120, framework=qiskit, class=3
from math import log2

from qiskit import QuantumCircuit
from qiskit.circuit.library import Diagonal


def create_diagonal_circuit(diag):
    """Create a QuantumCircuit with a Diagonal gate applied to all qubits."""
    n_qubits = int(log2(len(diag)))
    qc = QuantumCircuit(n_qubits)
    qc.append(Diagonal(diag), range(n_qubits))
    return qc
