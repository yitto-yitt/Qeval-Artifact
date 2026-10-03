# EVAL_META: task_id=120, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()


def create_diagonal_circuit(diag):
    diag = np.asarray(diag, dtype=complex)
    n = int(round(np.log2(len(diag))))
    mat = np.diag(diag)
    qubits = machine.qAlloc_many(n)
    circ = matrix_decompose(qubits, mat)
    return circ


machine.finalize()
