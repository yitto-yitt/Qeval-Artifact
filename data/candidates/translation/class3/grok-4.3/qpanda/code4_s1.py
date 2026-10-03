# EVAL_META: task_id=4, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QOracle

def create_unitary_from_matrix():
    matrix = [[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]
    circuit = QCircuit()
    circuit << QOracle([0, 1], matrix)
    return circuit
