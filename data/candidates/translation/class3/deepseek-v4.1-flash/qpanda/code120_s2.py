# EVAL_META: task_id=120, framework=qpanda, class=3
import math
from pyqpanda3.core import QCircuit, QGate, Qubit

def create_diagonal_circuit(diag):
    n = int(math.log2(len(diag)))
    qubits = [Qubit(i) for i in range(n)]
    size = 2 ** n
    matrix = [[0] * size for _ in range(size)]
    for i in range(size):
        matrix[i][i] = diag[i]
    gate = QGate(matrix, qubits)
    circuit = QCircuit()
    circuit << gate
    return circuit
