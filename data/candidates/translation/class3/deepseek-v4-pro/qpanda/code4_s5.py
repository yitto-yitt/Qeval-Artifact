# EVAL_META: task_id=4, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QuantumCircuit

def create_unitary_from_matrix():
    matrix = np.array([[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]], dtype=complex)
    circuit = QuantumCircuit(2)
    circuit.unitary(matrix, [0, 1])
    return circuit
