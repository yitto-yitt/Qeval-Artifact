# EVAL_META: task_id=120, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, QGate

def create_diagonal_circuit(diag):
    diag = np.asarray(diag, dtype=complex)
    n = int(np.log2(len(diag)))
    matrix = np.diag(diag)
    qc = QCircuit(n)
    qubits = list(range(n))
    qc << QGate(matrix, qubits)
    return qc
