# EVAL_META: task_id=4, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init()
q = machine.qAlloc_many(2)

def create_unitary_from_matrix():
    matrix = [[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]
    circuit = QCircuit()
    circuit.insert(Unitary(matrix, q[0], q[1]))
    return circuit

machine.finalize()
