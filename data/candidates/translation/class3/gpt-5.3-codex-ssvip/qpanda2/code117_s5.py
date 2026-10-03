# EVAL_META: task_id=117, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def decompose_unitary(unitary):
    u = np.array(unitary, dtype=complex)
    if u.shape != (4, 4):
        raise ValueError("unitary must be a 4x4 matrix")
    prog = pq.QProg()
    prog << pq.matrix_decompose(q, u.tolist())
    return prog

machine.finalize()
