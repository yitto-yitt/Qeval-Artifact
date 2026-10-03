# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import *

def inv_circuit(n):
    qvm = CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    if hasattr(qvm, "qAlloc_many"):
        q = qvm.qAlloc_many(n)
    elif hasattr(qvm, "qalloc_many"):
        q = qvm.qalloc_many(n)
    else:
        q = list(range(n))

    qc = QCircuit()

    for i in reversed(range(2)):
        qc << CNOT(q[i + 1], q[i + 3])

    for i in reversed(range(2)):
        qc << H(q[i + 1])

    if not hasattr(inv_circuit, "_qvm_keepalive"):
        inv_circuit._qvm_keepalive = []
    inv_circuit._qvm_keepalive.append(qvm)

    return qc
