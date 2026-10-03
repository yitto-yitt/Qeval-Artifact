# EVAL_META: task_id=120, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, matrix_decompose

def create_diagonal_circuit(diag):
    n = (len(diag)).bit_length() - 1
    dim = 1 << n
    mat = [[0j for _ in range(dim)] for _ in range(dim)]
    for i, v in enumerate(diag):
        mat[i][i] = complex(v)

    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)

    prog = QProg()
    prog << matrix_decompose(qubits, mat)

    return prog
