# EVAL_META: task_id=120, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QCircuit, QProg

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(16)


def create_diagonal_circuit(diag):
    diag = np.asarray(diag, dtype=complex)
    n = int(np.log2(len(diag)))
    qs = qubits[:n]

    dim = len(diag)
    mat = np.zeros((dim, dim), dtype=complex)
    for i in range(dim):
        mat[i, i] = diag[i]

    circ = QCircuit()
    circ << machine.matrix_decompose(qs, mat)
    return circ
