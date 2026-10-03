# EVAL_META: task_id=120, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, Qubit, QOracle

def create_diagonal_circuit(diag):
    n = int(np.log2(len(diag)))
    qubits = [Qubit(i) for i in range(n)]
    matrix = np.diag(diag).astype(complex)
    oracle = QOracle(matrix, qubits)
    circuit = QCircuit()
    circuit << oracle
    return circuit
