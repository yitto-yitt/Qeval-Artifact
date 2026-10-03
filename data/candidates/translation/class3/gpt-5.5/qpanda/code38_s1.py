# EVAL_META: task_id=38, framework=qpanda, class=3
from pyqpanda3.core import *


def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    qvm = CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    if hasattr(qvm, "qAlloc_many"):
        q = qvm.qAlloc_many(2)
    else:
        q = qvm.qalloc_many(2)

    qc = QCircuit()
    qc << H(q[0])
    qc << RZ(q[1], theta).control([q[0]])
    qc << H(q[1])
    qc << RY(q[0], theta).control([q[1]])
    return qc
