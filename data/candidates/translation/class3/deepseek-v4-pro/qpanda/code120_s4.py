# EVAL_META: task_id=120, framework=qpanda, class=3
import math
from pyqpanda3.core import QuantumCircuit

def create_diagonal_circuit(diag):
    n = int(math.log2(len(diag)))
    dim = 1 << n
    matrix = [[0j] * dim for _ in range(dim)]
    for i, val in enumerate(diag):
        matrix[i][i] = val
    qc = QuantumCircuit(n)
    qc.unitary(matrix, list(range(n)))
    return qc
