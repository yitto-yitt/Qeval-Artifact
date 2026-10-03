# EVAL_META: task_id=120, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)
def create_diagonal_circuit(diag):
    n = int(np.log2(len(diag)))
    qs = qubits[:n]
    prog = create_empty_qprog()
    unitary = np.diag(diag)
    gate = matrix_decompose(qs, unitary)
    prog << gate
    return prog
machine.finalize()
