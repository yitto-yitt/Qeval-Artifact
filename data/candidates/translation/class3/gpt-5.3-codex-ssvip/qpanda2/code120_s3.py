# EVAL_META: task_id=120, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_qpool = machine.qAlloc_many(64)

def create_diagonal_circuit(diag):
    diag = np.asarray(diag, dtype=complex)
    n = int(round(np.log2(len(diag))))
    if 2 ** n != len(diag):
        raise ValueError("Length of diag must be a power of 2.")
    q = _qpool[:n]
    prog = pq.QProg()
    mat = np.diag(diag).astype(complex)
    prog << pq.QOracle(q, mat)
    return prog

machine.finalize()
