# EVAL_META: task_id=5, framework=qpanda, class=2
from pyqpanda3.core import *


def create_state_prep():
    qvm = CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    if hasattr(qvm, "qAlloc_many"):
        qubits = qvm.qAlloc_many(2)
    else:
        qubits = qvm.qalloc_many(2)

    prog = QProg()
    prog << X(qubits[0]) << H(qubits[1]) << H(qubits[1])

    if not hasattr(create_state_prep, "_resources"):
        create_state_prep._resources = []
    create_state_prep._resources.append((qvm, qubits))

    return prog
