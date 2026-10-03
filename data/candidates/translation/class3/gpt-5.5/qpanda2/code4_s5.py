# EVAL_META: task_id=4, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
atexit.register(machine.finalize)

def create_unitary_from_matrix():
    matrix = [
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
    ]
    flat_matrix = [complex(x) for row in matrix for x in row]

    prog = QProg()
    try:
        prog << QOracle(qubits, matrix)
    except Exception:
        try:
            prog << QOracle(qubits, flat_matrix)
        except Exception:
            prog << matrix_decompose(qubits, matrix)
    return prog
