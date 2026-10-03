# EVAL_META: task_id=120, framework=qpanda2, class=3
import numpy as np
from pyqpanda import CPUQVM, QCircuit, QProg

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(16)


def create_diagonal_circuit(diag):
    diag = list(diag)
    n = int(np.log2(len(diag)))
    circ = QCircuit()
    dim = 2 ** n
    mat = np.zeros((dim, dim), dtype=complex)
    for i in range(dim):
        mat[i, i] = diag[i]
    q = qubits[:n]
    circ << matrix_decompose_circuit(mat, q)
    return circ


def matrix_decompose_circuit(mat, q):
    from pyqpanda import matrix_decompose
    return matrix_decompose(q, mat.flatten().tolist())


machine.finalize()
