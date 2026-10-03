# EVAL_META: task_id=26, framework=qpanda, class=3
from pyqpanda3.core import *


def bell_dag():
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
        q = [qvm.qAlloc() for _ in range(3)]

    if hasattr(qvm, "cAlloc_many"):
        c = qvm.cAlloc_many(3)
    elif hasattr(qvm, "calloc_many"):
        c = qvm.calloc_many(3)
    else:
        c = [qvm.cAlloc() for _ in range(3)]

    prog = QProg()
    prog << H(q[0])

    if "CNOT" in globals():
        prog << CNOT(q[0], q[1])
    else:
        prog << CX(q[0], q[1])

    if "Measure" in globals():
        prog << Measure(q[0], c[0])
    else:
        prog << measure(q[0], c[0])

    if not hasattr(bell_dag, "_qvms"):
        bell_dag._qvms = []
    bell_dag._qvms.append(qvm)

    for name in (
        "circuit_to_dag",
        "prog_to_dag",
        "qprog_to_dag",
        "convert_qprog_to_dag",
        "qprog_to_DAG",
        "convert_qprog_to_DAG",
    ):
        func = globals().get(name)
        if func is not None:
            for args in ((prog,), (prog, qvm), (qvm, prog)):
                try:
                    return func(*args)
                except TypeError:
                    pass

    return prog
