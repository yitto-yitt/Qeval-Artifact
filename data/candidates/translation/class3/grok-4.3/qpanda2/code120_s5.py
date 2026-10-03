# EVAL_META: task_id=120, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)
def create_diagonal_circuit(diag):
    from math import log2
    num_qubits = int(log2(len(diag)))
    q = qubits[:num_qubits]
    prog = QProg()
    prog << DiagonalMatrix(q, diag)
    return prog
machine.finalize()
