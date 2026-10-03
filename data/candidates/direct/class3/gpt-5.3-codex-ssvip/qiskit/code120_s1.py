# EVAL_META: task_id=120, framework=qiskit, class=3
import math
from qiskit import QuantumCircuit
from qiskit.circuit.library import Diagonal


def create_diagonal_circuit(diag):
    num_qubits = int(round(math.log2(len(diag)))) if len(diag) > 0 else 0
    if 2**num_qubits != len(diag):
        raise ValueError("Length of 'diag' must be a power of 2.")
    qc = QuantumCircuit(num_qubits)
    if num_qubits > 0:
        qc.append(Diagonal(diag), range(num_qubits))
    return qc
