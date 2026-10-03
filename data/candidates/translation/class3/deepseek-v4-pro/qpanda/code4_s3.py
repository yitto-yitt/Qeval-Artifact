# EVAL_META: task_id=4, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QGate

def create_unitary_from_matrix():
    matrix = [[0, 0, 0, 1],
              [0, 0, 1, 0],
              [1, 0, 0, 0],
              [0, 1, 0, 0]]
    gate = QGate(matrix)
    circuit = QCircuit()
    circuit.insert(gate)
    return circuit
