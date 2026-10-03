# EVAL_META: task_id=120, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import Diagonal
import math


def create_diagonal_circuit(diag):
    n = int(math.log2(len(diag)))
    qc = QuantumCircuit(n)
    qc.append(Diagonal(diag), range(n))
    return qc
