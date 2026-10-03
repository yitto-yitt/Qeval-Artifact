# EVAL_META: task_id=120, framework=qpanda2, class=3
import math
import cmath
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_qpool = machine.qAlloc_many(32)

def create_diagonal_circuit(diag):
    n = int(round(math.log2(len(diag))))
    if 2 ** n != len(diag):
        raise ValueError("Length of diag must be a power of 2.")
    qv = _qpool[:n]
    prog = pq.QProg()
    mat = np.diag(np.array(diag, dtype=complex))
    gate = pq.QOracle(qv, mat)
    prog.insert(gate)
    return prog

machine.finalize()
