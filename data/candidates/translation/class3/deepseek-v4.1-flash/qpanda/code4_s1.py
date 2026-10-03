# EVAL_META: task_id=4, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, unitary, qAlloc_many

def create_unitary_from_matrix():
    matrix = [[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]
    qubits = qAlloc_many(2)
    circuit = QCircuit()
    circuit << unitary(matrix, qubits)
    return circuit
