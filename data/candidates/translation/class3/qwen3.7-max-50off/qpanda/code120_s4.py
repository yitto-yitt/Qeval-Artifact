# EVAL_META: task_id=120, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, alloc_qubits, Diagonal
import math

def create_diagonal_circuit(diag):
    n = int(math.log2(len(diag)))
    qubits = alloc_qubits(n)
    qc = QCircuit()
    qc << Diagonal(diag)(qubits)
    return qc
