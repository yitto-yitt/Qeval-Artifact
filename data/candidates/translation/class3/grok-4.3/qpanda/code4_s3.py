# EVAL_META: task_id=4, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, QOracle

def create_unitary_from_matrix():
    matrix = [[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]
    qvm = CPUQVM()
    qvm.initQVM()
    qubits = qvm.qAllocMany(2)
    circuit = QCircuit()
    circuit << QOracle(qubits, matrix)
    return circuit
