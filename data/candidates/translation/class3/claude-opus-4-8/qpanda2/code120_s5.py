# EVAL_META: task_id=120, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QCircuit, QProg, matrix_decompose

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(16)

def create_diagonal_circuit(diag):
    diag = np.asarray(diag, dtype=complex)
    dim = len(diag)
    n = int(round(np.log2(dim)))
    mat = np.zeros((dim, dim), dtype=complex)
    for i in range(dim):
        mat[i, i] = diag[i]
    used = qubits[:n]
    circ = matrix_decompose(used, mat)
    prog = QProg()
    prog << circ
    return prog
