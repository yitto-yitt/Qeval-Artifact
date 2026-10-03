# EVAL_META: task_id=4, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QGate, qubit

def create_unitary_from_matrix():
    matrix = [[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]
    circuit = QCircuit()
    q = qubit(2)
    circuit << QGate("U4", matrix, q[0], q[1])
    return circuit
