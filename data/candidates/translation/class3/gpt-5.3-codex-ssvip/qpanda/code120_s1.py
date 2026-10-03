# EVAL_META: task_id=120, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, matrix_decompose

def create_diagonal_circuit(diag):
    n = 0
    length = len(diag)
    while (1 << n) < length:
        n += 1
    if (1 << n) != length:
        raise ValueError("Length of diag must be a power of 2.")
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)
    mat = [[0j for _ in range(length)] for _ in range(length)]
    for i, v in enumerate(diag):
        mat[i][i] = complex(v)
    prog = QProg()
    prog << matrix_decompose(qubits, mat)
    return prog
