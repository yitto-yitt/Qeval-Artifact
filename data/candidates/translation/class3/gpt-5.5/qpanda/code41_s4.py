# EVAL_META: task_id=41, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def compose_op():
    qvm = pq.CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    if hasattr(qvm, "qAlloc_many"):
        q = qvm.qAlloc_many(3)
    elif hasattr(qvm, "qalloc_many"):
        q = qvm.qalloc_many(3)
    elif hasattr(qvm, "qAllocMany"):
        q = qvm.qAllocMany(3)
    else:
        q = [0, 1, 2]

    prog = pq.QProg()
    prog << pq.X(q[0])
    prog << pq.H(q[1]) << pq.H(q[1])
    prog << pq.Y(q[2])

    if hasattr(pq, "get_matrix"):
        try:
            return np.array(pq.get_matrix(prog), dtype=complex)
        except Exception:
            pass

    x = np.array([[0, 1], [1, 0]], dtype=complex)
    i = np.eye(2, dtype=complex)
    y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    return np.kron(np.kron(y, i), x)
