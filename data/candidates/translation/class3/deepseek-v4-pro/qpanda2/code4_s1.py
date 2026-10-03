# EVAL_META: task_id=4, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_unitary_from_matrix():
    matrix = np.array([[0, 0, 0, 1],
                       [0, 0, 1, 0],
                       [1, 0, 0, 0],
                       [0, 1, 0, 0]], dtype=complex)
    circuit = QCircuit()
    circuit << QOracle(matrix)(q[0], q[1])
    return circuit

machine.finalize()
