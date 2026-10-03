# EVAL_META: task_id=4, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Gate

def create_unitary_from_matrix():
    matrix = [[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]
    circuit = QCircuit()
    qubits = circuit.qAllocMany(2)
    gate = Gate(matrix)
    circuit << gate(qubits[0], qubits[1])
    return circuit
