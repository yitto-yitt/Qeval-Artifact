# EVAL_META: task_id=4, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, Oracle

def create_unitary_from_matrix():
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)
    
    circuit = QCircuit()
    matrix = [[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]
    circuit << Oracle(qubits, matrix)
    return circuit
