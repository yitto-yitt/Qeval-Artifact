# EVAL_META: task_id=27, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, H, CNOT


def apply_op_back():
    qvm = CPUQVM()
    try:
        qvm.init_qvm()
    except AttributeError:
        pass

    q = qvm.qAlloc_many(3)
    try:
        c = qvm.cAlloc_many(3)
    except Exception:
        c = None

    prog = QProg()
    prog << H(q[0])
    prog << CNOT(q[0], q[1])
    prog << H(q[0])

    apply_op_back._qvm = qvm
    apply_op_back._qubits = q
    apply_op_back._cbits = c

    return prog
