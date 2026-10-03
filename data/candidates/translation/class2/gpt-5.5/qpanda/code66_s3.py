# EVAL_META: task_id=66, framework=qpanda, class=2
from numpy import arccos, sqrt
from pyqpanda3.core import *


def w_state():
    qvm = CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    if hasattr(qvm, "qAlloc_many"):
        q = qvm.qAlloc_many(3)
    elif hasattr(qvm, "qalloc_many"):
        q = qvm.qalloc_many(3)
    else:
        q_alloc = getattr(qvm, "qAlloc", getattr(qvm, "qalloc"))
        q = [q_alloc() for _ in range(3)]

    if hasattr(qvm, "cAlloc_many"):
        c = qvm.cAlloc_many(3)
    elif hasattr(qvm, "calloc_many"):
        c = qvm.calloc_many(3)
    else:
        c_alloc = getattr(qvm, "cAlloc", getattr(qvm, "calloc"))
        c = [c_alloc() for _ in range(3)]

    prog = QProg()
    prog << RY(q[0], 2 * arccos(1 / sqrt(3)))

    h_gate = H(q[1])
    try:
        prog << h_gate.control([q[0]])
    except TypeError:
        prog << h_gate.control(q[0])

    prog << CNOT(q[1], q[2])
    prog << CNOT(q[0], q[1])
    prog << X(q[0])

    prog << Measure(q[0], c[0])
    prog << Measure(q[1], c[1])
    prog << Measure(q[2], c[2])

    w_state._pyqpanda3_runtime = (qvm, q, c)
    return prog
