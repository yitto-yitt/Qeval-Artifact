# EVAL_META: task_id=4, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QGate, Qubit

def create_unitary_from_matrix():
    matrix = [[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]
    circuit = QCircuit()
    q0 = Qubit(0)
    q1 = Qubit(1)
    circuit << QGate.unitary(matrix, [q0, q1])
    return circuit
