# EVAL_META: task_id=120, framework=qpanda, class=3
from pyqpanda3.core import *

def create_diagonal_circuit(diag):
    n = 0
    size = len(diag)
    while (1 << n) < size:
        n += 1
    if (1 << n) != size:
        raise ValueError("Length of diag must be a power of 2.")

    mat = [[0j for _ in range(size)] for _ in range(size)]
    for i, v in enumerate(diag):
        mat[i][i] = complex(v)

    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n)

    prog = QProg()
    prog.insert(QOracle(q, mat))
    return prog
