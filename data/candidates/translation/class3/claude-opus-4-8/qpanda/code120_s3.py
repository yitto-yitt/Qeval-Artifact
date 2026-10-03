# EVAL_META: task_id=120, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, QGate, matrix_decompose

def create_diagonal_circuit(diag):
    diag = np.asarray(diag, dtype=complex)
    dim = len(diag)
    num_qubits = int(np.log2(dim))
    qubits = list(range(num_qubits))
    matrix = np.diag(diag)
    circuit = matrix_decompose(qubits, matrix)
    return circuit
