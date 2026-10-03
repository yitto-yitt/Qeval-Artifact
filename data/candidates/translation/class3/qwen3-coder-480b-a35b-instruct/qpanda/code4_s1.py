# EVAL_META: task_id=4, framework=qpanda, class=3
from pyqpanda import *

def create_unitary_from_matrix():
    matrix = [[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    circuit = QCircuit()
    circuit.insert(U4(matrix, qubits[0], qubits[1]))
    return circuit
