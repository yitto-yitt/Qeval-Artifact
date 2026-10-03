# EVAL_META: task_id=120, framework=qiskit, class=3
import math
from qiskit import QuantumCircuit
from qiskit.circuit.library import Diagonal


def create_diagonal_circuit(diag):
    num_qubits = int(math.log2(len(diag)))
    qc = QuantumCircuit(num_qubits)
    qc.append(Diagonal(diag), range(num_qubits))
    return qc
