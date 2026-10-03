# EVAL_META: task_id=4, framework=qpanda2, class=3
import atexit
import numpy as np
from pyqpanda import CPUQVM, QProg, matrix_decompose

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_unitary_from_matrix():
    matrix = np.array(
        [[0, 0, 0, 1],
         [0, 0, 1, 0],
         [1, 0, 0, 0],
         [0, 1, 0, 0]],
        dtype=complex
    )
    circuit = matrix_decompose(qubits, matrix)
    prog = QProg()
    prog << circuit
    return prog

atexit.register(machine.finalize)
