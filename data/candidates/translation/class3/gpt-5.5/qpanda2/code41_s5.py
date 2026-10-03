# EVAL_META: task_id=41, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)
atexit.register(machine.finalize)


def compose_op():
    prog = pq.QProg()
    prog << pq.X(q[0]) << pq.RZ(q[1], 0.0) << pq.Y(q[2])

    mat = None
    for name in ("get_matrix", "get_unitary", "get_qprog_matrix"):
        if hasattr(pq, name):
            mat = getattr(pq, name)(prog)
            break

    if mat is None:
        return prog

    mat = np.asarray(mat, dtype=complex)
    if mat.ndim == 1:
        dim = int(np.sqrt(mat.size))
        if dim * dim == mat.size:
            mat = mat.reshape((dim, dim))
    return mat
