# EVAL_META: task_id=120, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, MatrixGate
import math

def create_diagonal_circuit(diag):
    n = int(math.log2(len(diag)))
    qubits = Qubit(n)
    dim = 1 << n
    matrix = [[0] * dim for _ in range(dim)]
    for i in range(dim):
        matrix[i][i] = complex(diag[i])
    circuit = QCircuit()
    circuit << MatrixGate(matrix, qubits)
    return circuit
