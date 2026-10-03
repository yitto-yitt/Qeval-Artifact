# EVAL_META: task_id=4, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QVec, Unitary

def create_unitary_from_matrix():
    matrix = [[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]
    qc = QCircuit()
    q = QVec(2)
    qc << Unitary(matrix, q)
    return qc
