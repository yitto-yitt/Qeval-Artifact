# EVAL_META: task_id=120, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, matrix_decompose


def create_diagonal_circuit(diag):
    diag = np.asarray(diag, dtype=complex)
    n = int(round(np.log2(len(diag))))
    if 2**n != len(diag):
        raise ValueError("Length of diag must be a power of 2.")

    mat = np.diag(diag)

    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)

    prog = QProg()
    prog.insert(matrix_decompose(qubits, mat))

    return prog
