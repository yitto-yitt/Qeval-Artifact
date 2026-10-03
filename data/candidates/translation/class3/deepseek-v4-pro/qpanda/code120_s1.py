# EVAL_META: task_id=120, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, QGate, Allocate_qubit

def create_diagonal_circuit(diag):
    n = int(np.log2(len(diag)))
    qvec = Allocate_qubit(n)
    circuit = QCircuit()
    matrix = np.diag(diag).astype(complex)
    gate = QGate(matrix, "Diagonal")
    circuit.insert(gate(qvec))
    return circuit
