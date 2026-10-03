# EVAL_META: task_id=120, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, QGate, matrix_decompose

def create_diagonal_circuit(diag):
    diag = np.asarray(diag, dtype=complex)
    n = int(np.log2(len(diag)))
    U = np.diag(diag)
    qubits = list(range(n))
    circuit = matrix_decompose(qubits, U)
    return circuit
