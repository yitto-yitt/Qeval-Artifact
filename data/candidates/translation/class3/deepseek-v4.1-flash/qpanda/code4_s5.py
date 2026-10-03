# EVAL_META: task_id=4, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, qAlloc, unitary

def create_unitary_from_matrix():
    matrix = [[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]
    circuit = QCircuit()
    q = qAlloc(2)
    circuit << unitary(matrix, q)
    return circuit
