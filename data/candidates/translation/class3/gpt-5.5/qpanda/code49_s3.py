# EVAL_META: task_id=49, framework=qpanda, class=3
from pyqpanda3.core import *

def simple_elitzur_vaidman():
    qvm = CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    if hasattr(qvm, "qAlloc_many"):
        q = qvm.qAlloc_many(2)
    elif hasattr(qvm, "qalloc_many"):
        q = qvm.qalloc_many(2)
    elif hasattr(qvm, "allocate_qubits"):
        q = qvm.allocate_qubits(2)
    else:
        q = [qvm.qAlloc(), qvm.qAlloc()]

    prog = QProg()
    prog << H(q[0])

    if "CNOT" in globals():
        prog << CNOT(q[0], q[1])
    elif "CX" in globals():
        prog << CX(q[0], q[1])
    else:
        prog << X(q[1]).control([q[0]])

    prog << H(q[0])

    if not hasattr(simple_elitzur_vaidman, "_qvms"):
        simple_elitzur_vaidman._qvms = []
    simple_elitzur_vaidman._qvms.append(qvm)
    simple_elitzur_vaidman._qubits = q

    return prog
